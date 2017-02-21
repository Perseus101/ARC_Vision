import unittest
import time

import ARC
import filters
import cv2

class FilterTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.flight = ARC.Flight(157)
        self.targets = self.flight.all_targets()
        self.target_images = []
        
        for tgt in self.targets:
            if not ((tgt.target_type == 0) or (tgt.target_type == 1) or (tgt.target_type == None)):
                continue
            new_images = self.flight.images_near(tgt.coord, 50)
            self.target_images.extend(new_images)
        #Remove duplicate files
        self.target_images = dict((image.filename, image) for image in self.target_images).values()
        self.images = self.flight.all_images()
        
    def test_get_contours(self):
        for img, i in zip(self.target_images, range(len(self.target_images))):
            with self.subTest(i=i):
                
                start_time = time.time()
                ROIs = filters.get_contours(cv2.imread(img.high_quality_jpg), 300)
                self.assertLess((time.time()-start_time), 2) # Ensure the operation took less than 2 seconds
                self.assertLess(len(ROIs), 330)
                self.assertGreater(len(ROIs), 270)

    def test_high_pass_filter(self):
        return

if __name__ == '__main__':
    unittest.main()