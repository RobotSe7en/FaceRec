# FaceRec
FaceRec is a python script to recognize faces with [face_recognition](https://github.com/ageitgey/face_recognition).

The script [fr.py](https://github.com/RobotSe7en/FaceRec/blob/main/fr.py) can recognize faces in images according to the labeled images. It will write name of face into metadata of image by adding {"Xmp.xmp.Keywords": "name1,name2, name3,..."} to xmp. 

The labeled images can be uploaded to NAS. The name of each face of images can be found through [Photprism](https://github.com/photoprism/photoprism)'s index.
