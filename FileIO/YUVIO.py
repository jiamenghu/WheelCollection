'''
author : Menghu Jia
Data   : 2022/9/25
'''
import numpy as np

class YUV_IO():
    def __init():
        pass
    pass


def read_YUV_block(FileName,Width,Height,BitDepth,FrameID,BlockPosition,BlockSize,Numbers=1,ComponentID=[True,False,False],YUVFormat='420p'):
    '''
    FileName:文件名称
    '''
    if YUVFormat == '420p':
        CWidth,CHeight = Width//2, Height//2 
    elif YUVFormat == '444p':
        CWidth,CHeight = Width, Height
    else:
        raise Exception('YUVFormat not supported')

    if BitDepth == 8:
        pixel_bit = 1
        pixel_type = np.uint8
    elif BitDepth == 20:
        pixel_bit = 2
        pixel_type = np.int16
    else:
        raise Exception('BitDepth not supported') 
    

    Ysize, Cbsize, Crsize = Width*Height, CWidth*CHeight, CWidth*CHeight
    Y_Bytes_numbers, Cb_Bytes_numbers, Cr_Bytes_numbers = Ysize* pixel_bit,Cbsize* pixel_bit,Crsize* pixel_bit
    frame_Bytes_numbers =Y_Bytes_numbers + Cb_Bytes_numbers + Cr_Bytes_numbers

    assert (ComponentID[0] or ComponentID[1] or ComponentID[2]), "should read one component at least" 

    #if Y is read , BlockPosition is the position of Y, else it is the position of Chroma
    
    if isinstance(BlockSize, list):
        BlockWidth, BlockHeight = BlockSize[0], BlockSize[1]
    else:
        BlockWidth, BlockHeight = BlockSize, BlockSize     
    CBlockWidth, CBlockHeight = BlockWidth, BlockHeight 
   
    if ComponentID[0]:
        lx, ly = BlockPosition[0], BlockPosition[1]
        
        if ComponentID[1] or ComponentID[2]:
            cx, cy = lx//(Width//CWidth), ly//(Height//CHeight)
           
            CBlockWidth, CBlockHeight = BlockWidth//(Width//CWidth), BlockHeight//(Height//CHeight)

    else:
        cx, cy = BlockPosition[0], BlockPosition[1]
        CBlockWidth, CBlockHeight = BlockWidth, BlockHeight 


    YBlocksize, CbBlocksize, CrBlocksize = BlockHeight*BlockWidth, CBlockHeight*CBlockWidth, CBlockHeight*CBlockWidth

    Planes = {}
    if ComponentID[0]:
        Planes['Y'] = np.zeros((Numbers, BlockHeight, BlockWidth), dtype=pixel_type)
    if ComponentID[1]:
        Planes['Cb'] = np.zeros((Numbers, CBlockHeight, CBlockWidth), dtype=pixel_type)
    if ComponentID[2]:
        Planes['Cr'] = np.zeros((Numbers, CBlockHeight, CBlockWidth), dtype=pixel_type)

    #start read data
    try:
        with open(FileName, 'rb') as fp:
            fp.seek(int(frame_Bytes_numbers * FrameID ), 0)
            for fidx in range(Numbers):
                
                if ComponentID[0] :
                    fp.seek(int(pixel_bit*(ly*Width)), 1)
                    Planes['Y'][fidx, ...] = np.fromfile(fp, dtype=pixel_type, count=BlockHeight*Width).reshape(BlockHeight, Width)[...,lx:lx+BlockWidth]
                    fp.seek(int(pixel_bit*((Height-ly-BlockHeight)*Width)),1)
                else:
                    fp.seek(int(Y_Bytes_numbers), 1)
                
                if ComponentID[1] :
                    fp.seek(int(pixel_bit*(cy*CWidth)), 1)
                    Planes['Cb'][fidx, ...] = np.fromfile(fp, dtype=pixel_type, count=CBlockHeight*CWidth).reshape(CBlockHeight, CWidth)[...,cx:cx+CBlockWidth]
                    fp.seek(int(pixel_bit*((CHeight-cy-CBlockHeight)*CWidth)),1)
                else:
                    fp.seek(int(Cb_Bytes_numbers), 1)

                if ComponentID[2] :
                    fp.seek(int(pixel_bit*(cy*CWidth)), 1)
                    Planes['Cr'][fidx, ...] = np.fromfile(fp, dtype=pixel_type, count=CBlockHeight*CWidth).reshape(CBlockHeight, CWidth)[...,cx:cx+CBlockWidth]
                    fp.seek(int(pixel_bit*((CHeight-cy-CBlockHeight)*CWidth)),1)
                else:
                    fp.seek(int(Cr_Bytes_numbers), 1)

    except IOError as e:
        print('Unable to open %s : %s\n' %(FileName,e))
    except EOFError as e:
        print("can't read so many data")

    return Planes


def read_YUV_frames(FileName,Width,Height,BitDepth,FrameID,Numbers=1,ComponentID=[True,False,False],YUVFormat='420p'):
    
    if YUVFormat == '420p':
        CWidth,CHeight = Width//2, Height//2 
    elif YUVFormat == '444p':
        CWidth,CHeight = Width, Height
    else:
        raise Exception('YUVFormat not supported')

    if BitDepth == 8:
        pixel_bit = 1
        pixel_type = np.uint8
    elif BitDepth == 20:
        pixel_bit = 2
        pixel_type = np.int16
    else:
        raise Exception('BitDepth not supported') 
    
    Ysize, Cbsize, Crsize = Width*Height, CWidth*CHeight, CWidth*CHeight
    Y_Bytes_numbers, Cb_Bytes_numbers, Cr_Bytes_numbers = Ysize* pixel_bit,Cbsize* pixel_bit,Crsize* pixel_bit
    frame_Bytes_numbers =Y_Bytes_numbers + Cb_Bytes_numbers + Cr_Bytes_numbers

    assert (ComponentID[0] or ComponentID[1] or ComponentID[2]), "should read one component at least" 
    Planes = {}
    if ComponentID[0]:
        Planes['Y'] = np.zeros((Numbers, Height, Width), dtype=pixel_type)
    if ComponentID[1]:
        Planes['Cb'] = np.zeros((Numbers, CHeight, CWidth), dtype=pixel_type)
    if ComponentID[2]:
        Planes['Cr'] = np.zeros((Numbers, CHeight, CWidth), dtype=pixel_type)

    #start read data
    try:
        with open(FileName, 'rb') as fp:
            fp.seek(int(frame_Bytes_numbers*FrameID), 0)
            for fidx in range(Numbers):
                if ComponentID[0] :
                    Planes['Y'][fidx, ...] = np.fromfile(fp, dtype=pixel_type, count=Ysize).reshape(Height, Width)
                else:
                    fp.seek(int(Y_Bytes_numbers), 1)
                
                if ComponentID[1] :
                    Planes['Cb'][fidx, ...] = np.fromfile(fp, dtype=pixel_type, count=Cbsize).reshape(CHeight, CWidth)
                else:
                    fp.seek(int(Cb_Bytes_numbers), 1)

                if ComponentID[2] :
                    Planes['Cr'][fidx, ...] = np.fromfile(fp, dtype=pixel_type, count=Crsize).reshape(CHeight, CWidth)
                else:
                    fp.seek(int(Cr_Bytes_numbers), 1)

    except IOError as e:
        print('Unable to open %s : %s\n' %(FileName,e))
    except EOFError as e:
        print("can't read so many data")

    return Planes
    

def read_YUV_sequence():
    pass 

def write_YUV_frame():
    pass

def write_YUV_sequence():
    pass



if __name__ == "__main__":
    filename = "E:\work\Learn\seq\BasketballPass_416x240_50.yuv"
    from random import randint
    import time
    date1=time.time()
    ##test block and frame componence
    for i in range(10000):
        readY=True if randint(0,1) else False
        readCb= True if randint(0,1) else False
        readCr=True  if randint(0,1) else False
        if not (readY or readCb or readCr):
            continue
        framesid = randint(0,100) 
        totalframes =randint(1,50)
        blockpos=[randint(0,100),randint(0,50)]
        blocksize=[2*randint(1,32),2*randint(1,32)]
        #print('-----------------')
        #print(readY,readCb,readCr,framesid,totalframes,blockpos[0],blockpos[1],blocksize[0],blocksize[1])
        frames = read_YUV_frames(filename,416,240,8,framesid,totalframes ,[readY,readCb,readCr])
        planes = read_YUV_block(filename,416,240,8,framesid,blockpos,blocksize,totalframes ,[readY,readCb,readCr])
        # if readY :
        #     if (frames['Y'][0][blockpos[1]:blockpos[1]+blocksize[1],blockpos[0]:blockpos[0]+blocksize[0]] == planes['Y'][0]).all():
        #         pass #print(True)
        #     else:
        #         print(False)
    #print(planes)
    date2 = time.time()
    print((date2-date1))