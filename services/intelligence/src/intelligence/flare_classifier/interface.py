from shared.schemas.candidate import FusedFlareCandidate, FlareClass

class FlareClassifier:
    def classify(self, candidate: FusedFlareCandidate) -> FlareClass:
        """Maps peak flux (SoLEXS primary, HEL1OS as corroboration) to a
        GOES-equivalent class bin via calibrated flux-to-class thresholds."""
        pass
