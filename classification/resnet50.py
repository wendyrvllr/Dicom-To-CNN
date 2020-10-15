""" resnet50 model with keras"""

import numpy as np

from tensorflow.keras.layers import Input
from tensorflow.keras import layers
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.layers import ZeroPadding2D
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Dropout 
from tensorflow.keras.models import Model

def identity_block(input_tensor, kernel_size, filters, stage, block):
    """The identity block is the block that has no conv layer at shortcut.
    # Arguments
        input_tensor: input tensor
        kernel_size: defualt 3, the kernel size of middle conv layer at main path
        filters: list of integers, the filterss of 3 conv layer at main path
        stage: integer, current stage label, used for generating layer names
        block: 'a','b'..., current block label, used for generating layer names
    # Returns
        Output tensor for the block.
    """
    filters1, filters2, filters3 = filters

    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'
    bn_axis = 3
    x = Conv2D(filters1, (1, 1), name=conv_name_base + '2a')(input_tensor)
    x = BatchNormalization(axis = bn_axis, name=bn_name_base + '2a')(x)
    x = Activation('relu')(x)

    x = Conv2D(filters2, kernel_size,
               padding='same', name=conv_name_base + '2b')(x)
    x = BatchNormalization(axis = bn_axis,name=bn_name_base + '2b')(x)
    x = Activation('relu')(x)

    x = Conv2D(filters3, (1, 1), name=conv_name_base + '2c')(x)
    x = BatchNormalization(axis = bn_axis,name=bn_name_base + '2c')(x)

    x = layers.add([x, input_tensor])
    x = Activation('relu')(x)
    return x


def conv_block(input_tensor, kernel_size, filters, stage, block, strides=(2, 2)):
    """conv_block is the block that has a conv layer at shortcut
    # Arguments
        input_tensor: input tensor
        kernel_size: defualt 3, the kernel size of middle conv layer at main path
        filters: list of integers, the filterss of 3 conv layer at main path
        stage: integer, current stage label, used for generating layer names
        block: 'a','b'..., current block label, used for generating layer names
    # Returns
        Output tensor for the block.
    Note that from stage 3, the first conv layer at main path is with strides=(2,2)
    And the shortcut should have strides=(2,2) as well
    """
    filters1, filters2, filters3 = filters

    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'
    bn_axis = 3
    x = Conv2D(filters1, (1, 1), strides=strides,
               name=conv_name_base + '2a')(input_tensor)
    x = BatchNormalization(axis = bn_axis,name=bn_name_base + '2a')(x)
    x = Activation('relu')(x)

    x = Conv2D(filters2, kernel_size, padding='same',
               name=conv_name_base + '2b')(x)
    x = BatchNormalization(axis = bn_axis,name=bn_name_base + '2b')(x)
    x = Activation('relu')(x)

    x = Conv2D(filters3, (1, 1), name=conv_name_base + '2c')(x)
    x = BatchNormalization(name=bn_name_base + '2c')(x)

    shortcut = Conv2D(filters3, (1, 1), strides=strides,
                      name=conv_name_base + '1')(input_tensor)
    shortcut = BatchNormalization(axis = bn_axis, name=bn_name_base + '1')(shortcut)

    x = layers.add([x, shortcut])
    x = Activation('relu')(x)
    return x



def ResNet50(input_shape=(503, 136, 1)): #(1024, 256,1)
    """Instantiates the ResNet50 architecture.
    # Returns
        A Keras model instance.

    """
    x_input = Input(input_shape)
  

    x = ZeroPadding2D((3, 3))(x_input)
    x = Conv2D(64, (7, 7), strides=(2, 2), name='conv1')(x)
    x = BatchNormalization(name='bn_conv1')(x)
    x = Activation('relu')(x)
    x = MaxPooling2D((3, 3), strides=(2, 2))(x)

    x = conv_block(x, 3, [64, 64, 256], stage=2, block='a', strides=(1, 1))
    x = identity_block(x, 3, [64, 64, 256], stage=2, block='b')
    x = identity_block(x, 3, [64, 64, 256], stage=2, block='c')

    x = conv_block(x, 3, [128, 128, 512], stage=3, block='a')
    x = identity_block(x, 3, [128, 128, 512], stage=3, block='b')
    x = identity_block(x, 3, [128, 128, 512], stage=3, block='c')
    x = identity_block(x, 3, [128, 128, 512], stage=3, block='d')

    #x = conv_block(x, 3, [256, 256, 1024], stage=4, block='a')
    #x = identity_block(x, 3, [256, 256, 1024], stage=4, block='b')
    #x = identity_block(x, 3, [256, 256, 1024], stage=4, block='c')
    #x = identity_block(x, 3, [256, 256, 1024], stage=4, block='d')
    #x = identity_block(x, 3, [256, 256, 1024], stage=4, block='e')
    #x = identity_block(x, 3, [256, 256, 1024], stage=4, block='f')

    #x = conv_block(x, 3, [512, 512, 2048], stage=5, block='a')
    #x = identity_block(x, 3, [512, 512, 2048], stage=5, block='b')
    #x = identity_block(x, 3, [512, 512, 2048], stage=5, block='c')



    x = AveragePooling2D((7, 7), name='avg_pool')(x)
    x = Flatten()(x)

    #x = GlobalAveragePooling2D(name = 'avg_pool')(x)

    #x = Dense(2048, activation = 'relu', name = 'dense_1')(x)
    #x = Dropout(0.5, name = 'dropout_1')(x)
    #x = Activation('relu', name = 'activ_1')(x)

    #x = Dense(512, activation= 'relu', name = 'dense_1')(x)
    #x = Dropout(0.4, name = 'dropout_1')(x)
    #x = Activation('relu', name = 'activ_1')(x)

    x = Dense(256, activation= 'relu', name = 'dense_2')(x)
    x = Dropout(0.4, name = 'dropout_2')(x)
    x = Activation('relu', name = 'activ_2')(x)

    x = Dense(128, activation= 'relu', name = 'dense_3')(x)
    x = Dropout(0.4, name = 'dropout_3')(x)
    x = Activation('relu', name = 'activ_3')(x)


    #final output
    left_arm = Dense(2, activation='softmax', name='left_arm')(x)
    right_arm = Dense(2, activation='softmax', name = 'right_arm')(x)

    head = Dense(2, activation='softmax', name='head')(x)
    leg = Dense(2, activation='softmax', name='leg')(x)


    #create the Model
    model = Model(inputs = x_input, outputs = [head, leg, right_arm, left_arm], name='ResNet50')
    return model 


def predictions_decoding(predictions):
    neurones = 4
    predi = []
    for i in range(predictions[0].shape[0]):
        subliste = []
        for j in range(0, neurones): 
            liste = predictions[j][i].tolist()
            #print(liste)
            maxi = np.max(liste)
            index = liste.index(maxi)
            #print(index)
            if j == 0 : #head
                if index == 0 : 
                    subliste.append("Vertex")
                if index == 1 : 
                    subliste.append("Eyes")
                if index == 2 : 
                    subliste.append("Mouth")
            if j == 1 : #leg
                if index == 0 : 
                    subliste.append("Hips")
                if index == 1 : 
                    subliste.append("Knee")
                if index == 2 : 
                    subliste.append("Foot")
            if j == 2 : #right arm
                if index == 0 : 
                    subliste.append("down")
                if index == 1 : 
                    subliste.append("up")
            if j == 3 : #left arm
                if index == 0 : 
                    subliste.append("down")
                if index == 1 : 
                    subliste.append("up")

        predi.append(subliste)

    return predi