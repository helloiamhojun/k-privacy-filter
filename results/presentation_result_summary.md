# Result Summary

On the 300-example Korean evaluation set, the baseline OpenAI Privacy Filter achieved 0.5945 entity-level F1. Adding the Korean Regex Safety Net improved F1 to 0.6710 (+7.66 points), Critical Recall from 0.7626 to 0.8129 (+5.04 points), and reduced False Positive Rate from 0.3284 to 0.2529 (-7.55 points). Latency stayed almost unchanged at about 0.98-1.00 seconds per example on Colab T4.

Fine-tuning note:
Official `opf train` completed training and validation, but checkpoint saving repeatedly failed in Colab with interruption/SIGKILL. Therefore, the final demo uses the stable hybrid pipeline: baseline OPF plus deterministic Korean regex backup.
