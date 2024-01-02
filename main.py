
from option import args

import torch
import utility
import data
import loss
from trainer import Trainer
import warnings
warnings.filterwarnings('ignore')
import os
os.system('pip install einops')
import model
torch.manual_seed(args.seed)
checkpoint = utility.checkpoint(args)

checkpoint.args.test_only = True
checkpoint.args.dir_data = "CBSD68"
checkpoint.args.pretrain = "tmodel1_epoch_0.pt"
checkpoint.args.data_test = ["CBSD68"]
checkpoint.args.scale = [1]
checkpoint.args.denoise = True
checkpoint.args.cpu = False


def main():
    global model
    if checkpoint.ok:
        loader = data.Data(args)
        _model = model.Model(args, checkpoint)
        if args.pretrain != "":
            if 's3' in args.pretrain:
                import moxing as mox
                mox.file.copy_parallel(args.pretrain,"/cache/models/umtl.pt")
                args.pretrain = "/cache/models/ipt.pt"
            _model = torch.load(args.pretrain)
            # _model.model.load_state_dict(state_dict,strict = False)
        _loss = loss.Loss(args, checkpoint) if not args.test_only else None
        t = Trainer(args, loader, _model, _loss, checkpoint)
        t.test()
        checkpoint.done()
            


if __name__ == '__main__':
    main()
