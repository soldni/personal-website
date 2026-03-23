VENUE_SHORT_NAMES = {
    "AAAI Conference on Artificial Intelligence": "AAAI",
    "AAAI/ACM Conference on AI, Ethics, and Society": "AIES",
    "ACM Conference on Bioinformatics, Computational Biology, and Health Informatics": "ACM-BCB",
    "ACM International Conference on Information and Knowledge Management": "CIKM",
    "Annual Conference of the North American Chapter of the Association for Computational Linguistics": "NAACL",
    "Annual Meeting of the Association for Computational Linguistics": "ACL",
    "Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics": "AACL",
    "Conference of the European Chapter of the Association for Computational Linguistics": "EACL",
    "Conference on Computer Vision and Pattern Recognition": "CVPR",
    "Conference on Empirical Methods in Natural Language Processing": "EMNLP",
    "Conference on Fairness, Accountability, and Transparency": "FAccT",
    "Conference on Language Modeling": "COLM",
    "Conference on Neural Information Processing Systems": "NeurIPS",
    "European Conference on Information Retrieval": "ECIR",
    "International ACM SIGIR Conference on Research and Development in Information Retrieval": "SIGIR",
    "International Conference on Computational Linguistics": "COLING",
    "International Conference on Intelligent User Interfaces": "IUI",
    "International Conference on Learning Representations": "ICLR",
    "International Conference on Machine Learning": "ICML",
    "Journal of the Association for Information Science and Technology": "JASIST",
    "Nature": "Nature",
    "SIAM International Conference on Data Mining": "SDM",
    "Text REtrieval Conference": "TREC",
    "The Web Conference": "WWW",
    "Transactions on Machine Learning Research": "TMLR",
}


def venue_short_name(name: str) -> str:
    return VENUE_SHORT_NAMES.get(name, name)


def render_venue_text(entry: dict[str, str]) -> str:
    archiveprefix = entry.get("archiveprefix", "")
    eprint = entry.get("eprint", "")
    if archiveprefix and eprint:
        if entry.get("badge") == "preprint":
            return ""
        return f"{archiveprefix} {eprint}"

    if entry.get("journal"):
        parts = [venue_short_name(entry["journal"]), entry.get("year", "")]
        return " ".join(part for part in parts if part)

    if entry.get("school"):
        parts = [venue_short_name(entry["school"]), entry.get("year", ""), "PhD Thesis"]
        return " ".join(part for part in parts if part)

    if entry.get("booktitle"):
        parts = [venue_short_name(entry["booktitle"]), entry.get("year", ""), entry.get("venue_note", "")]
        return " ".join(part for part in parts if part)

    return ""
