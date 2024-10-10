import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import matplotlib.pyplot as plt

def extract_color_palette(image_path, num_colors=5):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image at {image_path}. Check the file path.")
        return
    
    # Convert the image to RGB (from BGR format used by OpenCV)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Reshape the image to a 2D array of pixels (each pixel is an RGB value)
    pixels = image_rgb.reshape(-1, 3)
    
    # Use KMeans to cluster the pixel colors
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    
    # Get the cluster centers (the most dominant colors)
    colors = kmeans.cluster_centers_
    
    # Get the percentage of each color by counting the occurrences of each label
    labels = kmeans.labels_
    label_counts = Counter(labels)
    
    # Sort the colors by the percentage in descending order
    sorted_colors = sorted(label_counts.items(), key=lambda x: x[1], reverse=True)
    color_palette = [colors[i].astype(int).tolist() for i, _ in sorted_colors]
    
    # Normalize the color percentages (optional, just for visualization)
    color_percentages = [count / len(labels) for _, count in sorted_colors]
    print(color_palette)

    return color_palette, color_percentages

def plot_color_palette(color_palette, color_percentages):
    plt.figure(figsize=(8, 2))
    plt.bar(range(len(color_palette)), color_percentages, color=[np.array(c) / 255 for c in color_palette])
    plt.xticks(range(len(color_palette)), [f'{p:.2%}' for p in color_percentages])
    plt.show()

# Example usage
# image_path = 'generatedImages\output_file_3.png'
# color_palette, color_percentages = extract_color_palette(image_path, num_colors=5)

# Display the color palette with their percentages
# print("Extracted Color Palette (sorted by percentage):")
# for i, (color, percentage) in enumerate(zip(color_palette, color_percentages)):
#     print(f"Color {i+1}: {color}, Percentage: {percentage:.2%}")

# # Plot the palette
# plot_color_palette(color_palette, color_percentages)

