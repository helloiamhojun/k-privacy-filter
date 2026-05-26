# Final Retrain Attempt Result

## Summary

A final OPF retraining attempt was executed before the final presentation.

## Result

- Training examples: 4,800
- Validation examples: 1,200
- Epochs: 1
- Train loss: 0.237742
- Validation loss: 0.140497
- Validation token accuracy: 0.9600
- Exit status: 137
- Failure point: checkpoint saving stage
- Final deployed system: OpenAI Privacy Filter + Regex Safety Net Hybrid

## Decision

The fine-tuned checkpoint was not used because the model weight file was not successfully saved.
The final presentation uses the reproducible Hybrid pipeline as the main system.
