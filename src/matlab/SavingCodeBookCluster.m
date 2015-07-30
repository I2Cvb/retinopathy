%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% BoF - Mojdeh - Guillaume - Sik - Desire 
%%% OCT images - Two vs all 
%%% UB - 10 - 06 - 15 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function SavingCodeBookCluster(mId, WIdx, CV)
addpath ../../toolbox/vlfeat-0.9.16/toolbox/
vl_setup
addpath ../../toolbox/basic_functions/
%addpath ../../toolbox/RF_Class_C/

filePath  = '/user1/le2i/gu5306le/Work/OCT_processing/'; 
featurePath = '/user1/le2i/gu5306le/Work/OCT_processing/features/'; 
path_to_save = '/user1/le2i/gu5306le/Work/OCT_processing/result/'; 
modelPath = '/user1/le2i/gu5306le/Work/OCT_processing/model/'; 

data = csv2cell(fullfile(filePath, 'data.csv'), 'fromfile'); 
dataname = data(2:end, 1); 
datalabel = data(2:end, 2); 
for i = 1 : length(datalabel)
    label(i) = str2num(cell2mat(datalabel(i)));
end
label(label == -1) = 0 ; 
mapsname = char('8ru', '16ru', '24ru'); 
mapsL = [3, 4 , 4]; 

numWords = [32]; 

model.quantizer = 'kdtree' ;
model.vocab = [];

    Idx = 1 : 32 ; 
    testIdx = [CV, CV+16]; 
    trainIdx = Idx ; 
    trainIdx(testIdx) =[]; 
    descrs = []; 
    train_data = []; 
    train_label = [];
    for fileId = 1 : length(trainIdx)
        filename = [cell2mat(dataname(trainIdx(fileId))) '_nlm_' mapsname(mId, 1:mapsL(mId)) '_LbpTopPatch3.mat']; 
        load(fullfile(featurePath, filename)); 
        %             for i  = 1 : length(Histogram)
        %                 tem = Histogram{i}; 
        %                 Histogram{i} = horzcat(tem(1,:), tem(2,:), tem(3,:));                  
        %             end 
        fileHist = cat(1, Histogram{:}); 
        fileHist = fileHist'; 
        descrs = [descrs, fileHist]; 
        train_label = [train_label, label(trainIdx(fileId))]; 
    end 

    descrs = single(descrs) ;
    vocab = vl_kmeans(descrs, numWords(WIdx), 'Initialization', 'plusplus', 'verbose', 'algorithm', 'elkan', 'NumRepetitions', 5 , 'MaxNumIterations', 1000) ;
    model.vocab = vocab; 
    if strcmp(model.quantizer, 'kdtree')
        model.kdtree = vl_kdtreebuild(vocab) ;
    end
    modelname = ['model3_' mapsname(mId, 1:mapsL(mId)) '_' num2str(numWords(WIdx)) '_' num2str(CV) '.mat']; 
    save(fullfile(modelPath, modelname), 'model'); 

