import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np

class TimeSeriesDataset(Dataset):
    def __init__(self, features, labels, seq_length=10):
        self.features = features
        self.labels = labels
        self.seq_length = seq_length

    def __len__(self):
        return len(self.features) - self.seq_length

    def __getitem__(self, idx):
        x = self.features[idx:idx + self.seq_length]
        y = self.labels[idx + self.seq_length - 1]
        return torch.tensor(x, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

class FlareLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim=64, num_layers=2):
        super(FlareLSTM, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x: (batch, seq_len, input_dim)
        out, _ = self.lstm(x)
        # We take the output of the last time step
        out = self.fc(out[:, -1, :])
        return self.sigmoid(out)

def train_pytorch_lstm(X_train, y_train, input_dim, epochs=10, batch_size=64, seq_length=10):
    dataset = TimeSeriesDataset(X_train.values, y_train.values, seq_length=seq_length)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = FlareLSTM(input_dim=input_dim)
    
    # For highly imbalanced data, we weight the positive class
    pos_weight = len(y_train[y_train==0]) / max(1, len(y_train[y_train==1]))
    
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    def weighted_binary_cross_entropy(output, target, weights=None):
        loss = nn.BCELoss(reduction='none')(output, target)
        if weights is not None:
            loss = loss * weights
        return loss.mean()
        
    model.train()
    for epoch in range(epochs):
        epoch_loss = 0
        for batch_x, batch_y in dataloader:
            optimizer.zero_grad()
            outputs = model(batch_x).squeeze()
            if outputs.dim() == 0:
                outputs = outputs.unsqueeze(0)
                
            weights = torch.ones_like(batch_y)
            weights[batch_y == 1] = pos_weight
            
            loss = weighted_binary_cross_entropy(outputs, batch_y, weights)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
            
        print(f"LSTM Epoch {epoch+1}/{epochs}, Loss: {epoch_loss/len(dataloader):.4f}")
        
    return model

def predict_pytorch_lstm(model, X_test, seq_length=10):
    model.eval()
    if isinstance(X_test, torch.Tensor):
        X_test_np = X_test.numpy()
    elif hasattr(X_test, 'values'):
        X_test_np = X_test.values
    else:
        X_test_np = X_test
        
    if len(X_test_np) < seq_length:
        pad_size = seq_length - len(X_test_np)
        X_test_np = np.vstack([np.zeros((pad_size, X_test_np.shape[1])), X_test_np])
        
    dataset = TimeSeriesDataset(X_test_np, np.zeros(len(X_test_np)), seq_length=seq_length)
    dataloader = DataLoader(dataset, batch_size=64, shuffle=False)
    
    preds = []
    with torch.no_grad():
        for batch_x, _ in dataloader:
            outputs = model(batch_x).squeeze()
            if outputs.dim() == 0:
                outputs = outputs.unsqueeze(0)
            preds.extend(outputs.numpy())
            
    padded_preds = np.zeros(len(X_test_np))
    if len(preds) > 0:
        padded_preds[seq_length:] = preds
        
    # Return to original size if we padded
    if hasattr(X_test, 'values') and len(X_test) < seq_length:
         padded_preds = padded_preds[-len(X_test):]
         
    return padded_preds
