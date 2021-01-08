import face_recognition
import os
from pyexiv2 import Image

def knownfaces(fpath, model='hog'):
	# Load the jpg files into numpy arrays
	file_list = os.listdir(fpath)
	try:
		file_list.remove('.DS_Store')
	except:
		pass
	names = []
	known_faces = []
	for f in file_list:
		names.append(f.split('.')[0])
		file = os.path.join(fpath, f)
		image_np = face_recognition.load_image_file(file, pixel=2000)
		face_loc = face_recognition.face_locations(image_np, model=model)
		face_encoding = face_recognition.face_encodings(image_np, known_face_locations=face_loc)[0]
		known_faces.append(face_encoding)
	print('faces loaded.')
	return names, known_faces


def get_file_path(fpath):
	file_list = []
	for home, dirs, files in os.walk(fpath):
		for filename in files:
			fullname = os.path.join(home, filename)
			file_list.append(fullname)
	return file_list

def face_rec(fpath, names, known_faces, model='hog'):
	unknown_images = get_file_path(fpath)
	count = 0
	total = len(unknown_images)
	for i in unknown_images:
		count += 1
		try:
			im = Image(i)
		except:
			print('Pass ' + i)
			continue
		# im_xmp = im.read_xmp()
		# if 'Xmp.xmp.Keywords' in im_xmp.keys():
		# 	continue
		final_labels = ''
		xmp_labels = dict()
		xmp_labels.setdefault('Xmp.xmp.Keywords', '')
		unknown = face_recognition.load_image_file(i, pixel=1000)
		face_loc = face_recognition.face_locations(unknown, model=model)
		unknown_face_encoding = face_recognition.face_encodings(unknown, known_face_locations=face_loc)
		for f in unknown_face_encoding:
			dis =face_recognition.face_distance(known_faces, f)
			min_dis = min(dis)
			if min_dis <= 0.5:
				idx = dis.tolist().index(min_dis)
				label = names[idx] + ','
				xmp_labels['Xmp.xmp.Keywords'] = xmp_labels['Xmp.xmp.Keywords'] + label
				im.modify_xmp(xmp_labels)
				final_labels = im.read_xmp()['Xmp.xmp.Keywords']
		print(str(count) + '/' + str(total) + '  ' + i + ' added labels: ' + str(final_labels))
		im.close()

if __name__ == '__main__':
	# 已知人物的照片的文件夹，文件名表示对应人物的姓名
	names, known_faces = knownfaces('C:/Users/Danny/Desktop/FaceRec/known', model='cnn')
	# 照片待识别的文件夹，识别之后会将人物姓名写入图片的metadata里的xmp，关键字为Xmp.xmp.Keywords
	face_rec('C:/Users/Danny/Desktop/FaceRec/unknown', names, known_faces, model='cnn')














