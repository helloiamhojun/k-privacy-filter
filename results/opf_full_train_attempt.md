# OPF Full Train Attempt

- train_examples: 4800
- validation_examples: 1200
- epochs: 1
- batch_size: 1
- grad_accum_steps: 8
- learning_rate: 1e-5
- train_loss: 0.269795
- val_loss: 0.144646
- val_token_accuracy: 0.9600
- result: training loop completed, but Colab interrupted during checkpoint saving

Decision:
Run a smaller 1000-example training job to obtain a saved checkpoint for demo/evaluation.
