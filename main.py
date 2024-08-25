# -*- coding:utf-8 -*-
# @Author: Peizhen Li 
# @Desc: None
import os
os.environ['TOKENIZERS_PARALLELISM']='false'
os.environ["TORCH_DISTRIBUTED_DEBUG"] = "DETAIL"
import asyncio
from subrouter import SubRouter


async def run_sub_router():
	sub_router = SubRouter()
	loop = asyncio.get_event_loop()
	print(f'task loop is running!!!')
	task1 = loop.create_task(sub_router.sub_vcap_data())
	task2 = loop.create_task(sub_router.route_vle_task())
	await asyncio.gather(task1, task2)


from facenet_pytorch import MTCNN
from PIL import Image
import numpy as np

face_detector = MTCNN(keep_all=True, post_process=False, select_largest=False)


def get_center_faces(img_arr):
	boxes, probs = face_detector.detect(img_arr)    # boxes: Nx4 array
	box_order = np.argsort(np.abs((boxes[:, 2] + boxes[:, 0]) /2 - 640.))  # [::-1]
	selected_boxes = boxes[0].reshape(-1, 4)
	faces = face_detector.extract(img_arr, selected_boxes, save_path=None)
	# faces = face_detector.extract(img_arr, selected_boxes, save_path='./assets/center_face.png')
	return faces

def test_mtcnn():
	import torch
	import cv2
	import os.path as osp
	cur_dir = osp.abspath(osp.dirname(__file__))
	print(f'cur dir: {cur_dir} \n *****')
	img_arr = np.asarray(Image.open(osp.join(cur_dir, 'assets/multipersons.jpg')))
	img_arr = cv2.resize(img_arr, dsize=(1280, 720), interpolation=cv2.INTER_AREA)  # (720, 1280, 3)
	print(f'img arr shape: {img_arr.shape}')
	# cv2.imwrite('./assets/resized_multi.png', img_arr)
	# raise ValueError('Penny stops here!!!')
	face_tensors = get_center_faces(img_arr)
	# debug_face = face_tensors[0].permute(1, 2, 0).numpy()
	# cv2.imwrite('./assets/debug_save_face.png', cv2.cvtColor(debug_face, cv2.COLOR_RGB2BGR))
	# print(f'face tesnors0 : {torch.sum(face_tensors[0])}, torch.max: {torch.max(face_tensors[0])}')
	# print(f'face tensors[0]: {face_tensors[0].shape}, {torch.permute(face_tensors[0], (1, 2, 0)).shape}')
	# print(f'face tensor 0: {face_tensors[0].permute(1,2,0).numpy().shape}')
	# cv2.imwrite('./assets/debug_save_face.png', face_tensors[0].permute(1,2,0).numpy())

	cv2.imwrite('./assets/debug_save_face.png', face_tensors[0].permute(1,2,0).numpy())

	print(f'shape face tensors: {face_tensors.shape}')  # torch.Size([1, 3, 160, 160])




def test_emotion_response():
	from models import vle_model
	from utils import diag_buffer
	diag_buffer.update_dialogue(b'how are you? ')
	diag_buffer.update_dialogue(b'nice to meet you!')
	diag_buffer.update_dialogue(b'I really hate you!')
	diag_buffer.update_dialogue(b'Could you tell me your name?')
	diag_buffer.update_dialogue(b'I do not understand what you meant')
	anim = vle_model.get_emotion_response(0, 0)
	print(anim)

	pass

if __name__ == "__main__":
	# test_emotion_response()
	# test_mtcnn()
	asyncio.run(run_sub_router())
   