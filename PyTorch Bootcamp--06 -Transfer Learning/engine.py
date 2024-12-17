"""
Contains functions for training and testing a PyTorch model.
"""
import torch
from torchmetrics import Accuracy

from typing import Dict, List, Tuple

def train_step(model: torch.nn.Module, 
               dataloader: torch.utils.data.DataLoader, 
               loss_fn: torch.nn.Module, 
               optimizer: torch.optim.Optimizer) -> Tuple[float, float]:
    
    """Trains a PyTorch model for a single epoch.
    
    Turns a target PyTorch model to training mode and then
    runs through all of the required training steps (forward
    pass, loss calculation, optimizer step).

    Args:
    model: A PyTorch model to be trained.
    dataloader: A DataLoader instance for the model to be trained on.
    loss_fn: A PyTorch loss function to minimize.
    optimizer: A PyTorch optimizer to help minimize the loss function.

    Returns:
    A tuple of training loss and training accuracy metrics.
    In the form (train_loss, train_accuracy). For example:

    (0.1112, 0.8743)
    """
    
    accuracy = Accuracy(task="multiclass", num_classes=3)
    
    model.train()
    
    train_loss, train_acc = 0, 0

    for batch, (X, y) in enumerate(dataloader):
        y_pred = model(X)
        
        loss = loss_fn(y_pred, y)
        train_loss += loss.item() 
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        y_pred_class = torch.argmax(torch.softmax(y_pred, dim=1), dim=1)
        
        train_acc += accuracy(y_pred_class, y)

    train_loss = train_loss / len(dataloader)
    train_acc = train_acc / len(dataloader)
    
    return train_loss, train_acc

def test_step(model: torch.nn.Module, 
              dataloader: torch.utils.data.DataLoader, 
              loss_fn: torch.nn.Module) -> Tuple[float, float]:
    """Tests a PyTorch model for a single epoch.

    Turns a target PyTorch model to "eval" mode and then performs
    a forward pass on a testing dataset.

    Args:
    model: A PyTorch model to be tested.
    dataloader: A DataLoader instance for the model to be tested on.
    loss_fn: A PyTorch loss function to calculate loss on the test data.

    Returns:
    A tuple of testing loss and testing accuracy metrics.
    In the form (test_loss, test_accuracy). For example:

    (0.0223, 0.8985)
    """
    
    accuracy = Accuracy(task="multiclass", num_classes=3)
    
    model.eval() 

    test_loss, test_acc = 0, 0

    with torch.inference_mode():
        for batch, (X, y) in enumerate(dataloader):
            test_pred_logits = model(X)
            test_pred_labels = torch.argmax(torch.softmax(test_pred_logits, dim=1), dim=1)
            loss = loss_fn(test_pred_logits, y)
            
            test_loss += loss.item()            
            test_acc += accuracy(test_pred_labels, y)
    
    test_loss = test_loss / len(dataloader)
    test_acc = test_acc / len(dataloader)
    
    return test_loss, test_acc

# def train(model: torch.nn.Module, 
#           train_dataloader: torch.utils.data.DataLoader, 
#           test_dataloader: torch.utils.data.DataLoader, 
#           optimizer: torch.optim.Optimizer,
#           loss_fn: torch.nn.Module,
#           epochs: int) -> Dict[str, List]:
#     """Trains and tests a PyTorch model.

#     Passes a target PyTorch models through train_step() and test_step()
#     functions for a number of epochs, training and testing the model
#     in the same epoch loop.

#     Calculates, prints and stores evaluation metrics throughout.

#     Args:
#     model: A PyTorch model to be trained and tested.
#     train_dataloader: A DataLoader instance for the model to be trained on.
#     test_dataloader: A DataLoader instance for the model to be tested on.
#     optimizer: A PyTorch optimizer to help minimize the loss function.
#     loss_fn: A PyTorch loss function to calculate loss on both datasets.
#     epochs: An integer indicating how many epochs to train for.

#     Returns:
#     A dictionary of training and testing loss as well as training and
#     testing accuracy metrics. Each metric has a value in a list for 
#     each epoch.
#     In the form: {train_loss: [...],
#               train_acc: [...],
#               test_loss: [...],
#               test_acc: [...]} 
#     For example if training for epochs=2: 
#              {train_loss: [2.0616, 1.0537],
#               train_acc: [0.3945, 0.3945],
#               test_loss: [1.2641, 1.5706],
#               test_acc: [0.3400, 0.2973]} 
#     """
#     results = {"train_loss": [],
#                "train_acc": [],
#                "test_loss": [],
#                "test_acc": []
#     }
    
#     for epoch in range(epochs):
        
#         train_loss, train_acc = train_step(model=model,
#                                            dataloader=train_dataloader,
#                                            loss_fn=loss_fn,
#                                            optimizer=optimizer)
        
#         test_loss, test_acc = test_step(model=model,
#                                         dataloader=test_dataloader,
#                                         loss_fn=loss_fn)
        
#         print(f"Epoch: {epoch+1} | train_loss: {train_loss:.4f} | train_acc: {train_acc:.4f} |"
#           f"test_loss: {test_loss:.4f} | " f"test_acc: {test_acc:.4f}")
        
#         results["train_loss"].append(train_loss)
#         results["train_acc"].append(train_acc)
#         results["test_loss"].append(test_loss)
#         results["test_acc"].append(test_acc)
#     return results