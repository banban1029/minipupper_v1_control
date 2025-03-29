import torch

print(torch.__version__)
# 1.7.1

print(torch.cuda.is_available())
# True

print(torch.cuda.device_count())

print(torch.cuda.current_device())
# 0
