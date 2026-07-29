from dataclasses import asdict, dataclass


@dataclass
class Finding:
    file: str
    line: int
    column: int
    contextType: str
    findingType: str
    matchedText: str
    canonicalTarget: str = ""
    confidence: float = 0.0
    distancePoints: int = 100
    suggestedAction: str = "flag_only"
    proposedPatch: str = ""
    requiresHumanRuling: bool = True
    reason: str = ""
    protected: bool = False
    registryId: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class ScanResult:
    files_scanned: int
    findings: list[Finding]

    def to_dict(self):
        return {"summary": summarize(self), "findings": [f.to_dict() for f in self.findings]}


def summarize(result: ScanResult):
    fs = result.findings
    return {
        "filesScanned": result.files_scanned,
        "staleMasterEquationCandidates": sum(f.findingType == "retired_equation" for f in fs),
        "safeExactReplacements": sum(f.suggestedAction == "auto_fix" and not f.protected for f in fs),
        "requiresHumanRuling": sum(f.requiresHumanRuling for f in fs),
        "protectedRawOrStoryFragments": sum(f.protected for f in fs),
        "emojiOrMojibakeIssues": sum(f.findingType in {"emoji", "mojibake"} for f in fs),
        "htmlPagesNeedingReview": len({f.file for f in fs if f.contextType == "html"}),
    }
