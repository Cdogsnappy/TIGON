import os
# import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from matplotlib import pyplot as plt

from utility import *


    
    
if __name__ == '__main__':
    args=create_args()
    
    
    torch.enable_grad()
    random.seed(args.seed)
    torch.manual_seed(args.seed)

    device = torch.device('cuda:' + str(args.gpu)
                            if torch.cuda.is_available() else 'cpu')
    # load dataset
    data_train = loaddata(args,device)
    integral_time = args.timepoints

    time_pts = range(len(data_train))
    leave_1_out = []
    train_time = [x for i,x in enumerate(time_pts) if i!=leave_1_out]


    # model
    if args.solver != 'flow':
        func = UOT(in_out_dim=data_train[0].shape[1], hidden_dim=args.hidden_dim,n_hiddens=args.n_hiddens,device=device,activation=args.activation,solver=args.solver).to(device)
    else:
        func = UOTFlow(in_out_dim=data_train[0].shape[1], hidden_dim=args.hidden_dim, n_hiddens=args.n_hiddens, activation='TimeTanh')
    
    if args.save_dir is not None:
        if not os.path.exists(args.save_dir):
            os.makedirs(args.save_dir)
        ckpt_path = os.path.join(args.save_dir, 'ckpt_itr2000.pth')
        if os.path.exists(ckpt_path):
            checkpoint = torch.load(ckpt_path,map_location=torch.device('cpu'))
            '''
            plt.plot(checkpoint["LOSS"])
            plt.xlabel('Iteration')
            plt.ylabel('Loss')
            plt.show()
            '''
            func.load_state_dict(checkpoint['func_state_dict'])
            print('Loaded ckpt from {}'.format(ckpt_path))
    plot = plot_3d_flow if args.solver == 'flow' else plot_3d

    # generate the plot of trajecotry
    plot(func,data_train,train_time,integral_time,args,device)
    # Average Jacobian matrix of cells at day 0
    plot_jac_v(func,data_train[0],0,'Average_jac_d0.pdf',['UMAP1','UMAP1','UMAP1'],args,device)
    # Average gradients of growth rate of cells at day 0
    plot_grad_g(func,data_train[0],0,'Average_grad_d0.pdf',['UMAP1','UMAP1','UMAP1'],args,device)
    
