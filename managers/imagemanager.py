import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap

class ImageManager:
    _instance = None

    @staticmethod
    def getInstance():
        if ImageManager._instance is None:
            ImageManager()
        return ImageManager._instance

    def __init__(self):
        if ImageManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ImageManager._instance = self
            self.image_cache = {}
            self.load_images()

    def load_images(self):
        cwd = os.getcwd()
        images_path = os.path.join(cwd, 'resources', 'images')
        if not os.path.exists(images_path):
            raise Exception(f"Images path '{images_path}' does not exist")

        for root, _, files in os.walk(images_path):
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    file_path = os.path.join(root, file)
                    image_name = os.path.splitext(os.path.basename(file_path))[0]
                    self.image_cache[image_name] = QPixmap(file_path)

    def get_image(self, image_name):
        return self.image_cache.get(image_name, None)

# Usage example
if __name__ == "__main__":
    app = QApplication(sys.argv)
    image_manager = ImageManager.getInstance()

    # Test the image manager
    test_image = image_manager.get_image('cnu')
    if test_image:
        print(f"Image 'cnu' loaded successfully")
    else:
        print(f"Image 'cnu' not found")

    sys.exit(app.exec())
