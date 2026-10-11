"""Optional CPU toy regression; no model downloads."""
import torch
torch.manual_seed(7)
x=torch.linspace(-1,1,8).reshape(-1,1)
y=2*x+1
model=torch.nn.Linear(1,1)
optimizer=torch.optim.SGD(model.parameters(),lr=0.1)
for _ in range(400):
    optimizer.zero_grad()
    loss=torch.nn.functional.mse_loss(model(x),y)
    loss.backward()
    optimizer.step()
model.eval()
with torch.no_grad():
    test=torch.tensor([[-0.75],[0.15],[0.85]])
    error=torch.nn.functional.mse_loss(model(test),2*test+1)
print("weight",model.weight.item(),"bias",model.bias.item())
print("training_mse",loss.item(),"test_mse",error.item())
