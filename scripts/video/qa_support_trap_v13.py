#!/usr/bin/env python3
"""Verify the final redundancy cuts and red-free native hold."""
import qa_support_trap_v12 as qa
import build_support_trap_v13
import cv2
if __name__=='__main__':
    qa.main()
    # Empty third-column border must contain no red outline, including its cap.
    im=cv2.imread(str(qa.b.OUT/'qa'/'003885.jpg'))
    region=im[170:635,820:1155].astype('int16')
    blue,green,red=[region[:,:,i] for i in range(3)]
    count=int(((red-green>22)&(red-blue>22)).sum())
    assert count==0,count
    print('Third-column border: zero red-outline pixels.',flush=True)
