# %% 1- Load and Preprocess the Data
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Define data transformations
transform = transforms.Compose([
    transforms.ToTensor(),  # Convert images to tensors
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # Normalize RGB channels
])

# Load CIFAR-10 dataset
batch_size = 64
trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
train_loader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True)

testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
test_loader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False)

# Function to show some random images from CIFAR-10
def show_random_samples(loader, classes):
    data_iter = iter(loader)
    images, labels = next(data_iter)

    fig, axes = plt.subplots(1, 5, figsize=(10, 5))
    for i, ax in enumerate(axes):
        img = images[i] / 2 + 0.5  # Unnormalize
        img = img.permute(1, 2, 0).numpy()
        ax.imshow(img)
        ax.set_title(classes[labels[i].item()])
        ax.axis('off')
    plt.show()

# Split training data into train and validation sets
train_size = int(0.8 * len(trainset))
val_size = len(trainset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(trainset, [train_size, val_size])

train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=batch_size, shuffle=False)


# Define CIFAR-10 classes


classes = ['airplane', 'automobile', 'bird', 'cat', 'deer',
          'dog', 'frog', 'horse', 'ship', 'truck']

# Display sample images
show_random_samples(train_loader, classes)

# %% 2- Define the CNN Model
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        # First block
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.pool1 = nn.MaxPool2d(2)
        # Second block
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.conv4 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm2d(128)
        self.pool2 = nn.MaxPool2d(2)
        # Fully connected layers
        self.fc1 = nn.Linear(128 * 8 * 8, 512)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(512, 10)
        
    def forward(self, x):
        # First block
        x = self.bn1(torch.relu(self.conv1(x)))
        x = self.bn2(torch.relu(self.conv2(x)))
        x = self.pool1(x)
        # Second block
        x = self.bn3(torch.relu(self.conv3(x)))
        x = self.bn4(torch.relu(self.conv4(x)))
        x = self.pool2(x)
        # Fully connected
        x = torch.flatten(x, 1)
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

def class_accuracy(model, test_loader, classes):
    class_correct = [0.0] * 10
    class_total = [0.0] * 10
    
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            c = (predicted == labels).squeeze()
            for i in range(labels.size(0)):
                label = labels[i]
                class_correct[label] += c[i].item()
                class_total[label] += 1
    
    for i in range(10):
        print(f'Accuracy of {classes[i]}: {100 * class_correct[i] / class_total[i]:.2f}%')


# Initialize Model
model = CNN().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# %% 3- Training the CNN
def train_model(model, train_loader, val_loader, epochs, early_stop_patience, lr_patience):
    train_losses = []
    val_losses = []
    val_accuracies = []
    
    # Variables for early stopping
    best_val_loss = float('inf')
    best_model_state = None
    early_stop_counter = 0
    
    # Store the initial learning rate
    initial_lr = optimizer.param_groups[0]['lr']
    current_lr = initial_lr
    
    # Learning rate scheduler
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, 
        mode='min',           
        factor=0.1,           
        patience=lr_patience,  
        verbose=True,         
        min_lr=1e-6           
    )
    
    for epoch in range(epochs):
        # Training phase
        model.train()
        running_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        
        avg_train_loss = running_loss / len(train_loader)
        train_losses.append(avg_train_loss)
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        avg_val_loss = val_loss / len(val_loader)
        val_accuracy = 100 * correct / total
        
        val_losses.append(avg_val_loss)
        val_accuracies.append(val_accuracy)
        
        # Step the scheduler based on validation loss
        scheduler.step(avg_val_loss)
        
        # Get current learning rate and check if it changed
        new_lr = optimizer.param_groups[0]['lr']
        if new_lr != current_lr:
            print(f"\n{'='*50}")
            print(f"LEARNING RATE DECREASED: {current_lr:.6f} -> {new_lr:.6f}")
            print(f"{'='*50}\n")
            current_lr = new_lr
        
        print(f"Epoch {epoch+1}/{epochs}, Train Loss: {avg_train_loss:.4f}, Val Loss: {avg_val_loss:.4f}, Val Accuracy: {val_accuracy:.2f}%, LR: {current_lr:.6f}")
        
        # Early stopping logic
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            best_model_state = model.state_dict().copy()
            early_stop_counter = 0
        else:
            early_stop_counter += 1
            if early_stop_counter >= early_stop_patience:
                print(f"\n{'='*50}")
                print(f"EARLY STOPPING triggered after {epoch+1} epochs")
                print(f"{'='*50}\n")
                break
    
    # Load the best model state (if early stopping was triggered)
    if best_model_state is not None:
        model.load_state_dict(best_model_state)
    
    return train_losses, val_losses, val_accuracies

# Now store the losses and accuracies
train_losses, val_losses, val_accuracies = train_model(
    model, 
    train_loader, 
    val_loader, 
    epochs=20,
    early_stop_patience=3,  # Clear name for early stopping patience
    lr_patience=2           # Clear name for learning rate scheduler patience
 
) #this is where the function is called!!
print("Training Finished!!!")

# Plot the Loss Curves
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(train_losses, label='Training Loss', color='blue')
plt.plot(val_losses, label='Validation Loss', color='red')
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("Loss Curves")
plt.legend()

# Plot the Validation Accuracy
plt.subplot(1, 2, 2)
plt.plot(val_accuracies, label='Validation Accuracy', color='green')
plt.xlabel("Epochs")
plt.ylabel("Accuracy (%)")
plt.title("Validation Accuracy")
plt.legend()
plt.tight_layout()
plt.show()

# %% 4- Evaluate the CNN
def evaluate_model(model, test_loader):
    correct, total = 0, 0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    print(f"Test Accuracy: {100 * correct / total:.2f}%")

evaluate_model(model, test_loader)

# %% 5- Show Predictions on Random Test Images
import random

def show_predictions(model, test_loader, classes, num_samples=5):
    data_iter = iter(test_loader)
    images, labels = next(data_iter)

    fig, axes = plt.subplots(1, num_samples, figsize=(10, 5))
    for i, ax in enumerate(axes):
        img = images[i] / 2 + 0.5  # Unnormalize
        img = img.permute(1, 2, 0).numpy()

        with torch.no_grad():
            outputs = model(images[i:i+1].to(device))
            predicted_label = torch.argmax(outputs, 1).item()

        ax.imshow(img)
        ax.set_title(f"True: {classes[labels[i].item()]}\nPred: {classes[predicted_label]}", 
                     color='green' if predicted_label == labels[i].item() else 'red')
        ax.axis('off')
    plt.show()

show_predictions(model, test_loader, classes)

"""# %% 6- Visualize Filters of First Conv Layer
def visualize_filters(model):
    filters = model.conv1.weight.data.cpu().numpy()
    
    fig, axes = plt.subplots(4, 8, figsize=(8, 4))
    for i, ax in enumerate(axes.flat):
        if i < filters.shape[0]:
            img = filters[i].transpose(1, 2, 0)
            ax.imshow(img)
            ax.axis('off')
    plt.show()

visualize_filters(model)"""

# %%
