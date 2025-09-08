#!/usr/bin/env python3
"""
Test script for media upload functionality
"""
import requests
import os
from pathlib import Path

def test_media_upload():
    """Test the media upload endpoint"""
    
    # Create a test image file
    test_file_path = Path("test_image.jpg")
    with open(test_file_path, "wb") as f:
        # Create a minimal JPEG header (just for testing)
        f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' \",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9')
    
    try:
        # Test data
        data = {
            'rating': 5,
            'content': '테스트 리뷰입니다. 이미지와 함께 업로드합니다.',
            'verified_purchase': True
        }
        
        # Test file
        files = {
            'media_files': ('test_image.jpg', open(test_file_path, 'rb'), 'image/jpeg')
        }
        
        # Make request
        response = requests.post(
            'http://localhost:8000/api/products/PROD-001/reviews',
            data=data,
            files=files
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Media upload test passed!")
        else:
            print("❌ Media upload test failed!")
            
    except Exception as e:
        print(f"❌ Test error: {e}")
    finally:
        # Cleanup
        if test_file_path.exists():
            test_file_path.unlink()
        try:
            files['media_files'][1].close()
        except:
            pass

if __name__ == "__main__":
    test_media_upload()