%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% BoF - Mojdeh - Guillaume - Sik - Desire 
%%% OCT images - Two vs all 
%%% UB - 10 - 06 - 15 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
function classification_TopLbpPatch_BoF_Cluster(mId, WId, CV)
    addpath ../../toolbox/vlfeat-0.9.16/toolbox/
    vl_setup
    addpath ../../toolbox/basic_functions/
    addpath ../../toolbox/RF_Class_C/
    

    filePath  = '/media/lemaitre/My Passport/PhD/Coding/OrganizedCode/OCT_processing/'; 
    featurePath = '/media/lemaitre/My Passport/PhD/Coding/OrganizedCode/OCT_processing/features/'; 
    path_to_save = '/media/lemaitre/My Passport/PhD/Coding/OrganizedCode/OCT_processing/result/'; 
    modelPath = '/media/lemaitre/My Passport/PhD/Coding/OrganizedCode/OCT_processing/model/'; 

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
    ntree = [100]; 
    modelname = ['model3_'  mapsname(mId, 1:mapsL(mId)) '_' num2str(numWords(WId)) '_' num2str(CV) '.mat']; 
    load(fullfile(modelPath, modelname)); 
    pred_label = zeros(2,1); 
    Idx = 1 : 32 ; 
    testIdx = [CV, CV+16]; 
    trainIdx = Idx ; 
    trainIdx(testIdx) =[]; 
    train_label = [];

    % --------------------------------------------------------------------
    %     Compute spatial histograms - Train Set 
    % --------------------------------------------------------------------
    hists = {} ;

    for fileId = 1 : length(trainIdx)
       filename = [cell2mat(dataname(trainIdx(fileId))) '_nlm_' mapsname(mId, 1:mapsL(mId)) '_LbpTopPatch3.mat']; 
    %                        filename = [cell2mat(dataname(trainIdx(fileId))) '_' mapsname(mId, 1:mapsL(mId)) '_Duke_LbpTopPatch3.mat']; 

       load(fullfile(featurePath, filename)); 
    %  
%     if fileId ==  28
%            fileHist = []; 
%            for j = 1 : length(Histogram)
%                tem = double(Histogram{j}); 
%                tem = tem'; 
%                fileHist= [fileHist, tem]; 
%            end
%     end
    %                        for i  = 1 : length(Histogram)
    %                             tem = Histogram{i}; 
    %                             Histogram{i} = horzcat(tem(1,:), tem(2,:), tem(3,:));                    
    %                        end 
        fileHist = cat(1, Histogram{:}); 
        fileHist = fileHist'; 

       hists{fileId} = getImageDescriptor(model, fileHist);
       train_label = [train_label, label(trainIdx(fileId))]; 
    end 
    hists = cat(2, hists{:}) ;

    % --------------------------------------------------------------------
    %    Compute feature map - this step could be removed
    % --------------------------------------------------------------------

    %Train_psix = vl_homkermap(hists, 1, 'kchi2', 'gamma', .5) ;
    %Train_data =  FeatureScale(Train_psix') ; 
    train_data = hists'; 
    train_label = train_label'; 


    test_label = []; 
    % --------------------------------------------------------------------
    %     Compute spatial histograms - Test Set 
    % --------------------------------------------------------------------
    hists = {} ;

    for fileId = 1 : length(testIdx)
       filename = [cell2mat(dataname(testIdx(fileId))) '_nlm_' mapsname(mId, 1:mapsL(mId)) '_LbpTopPatch3.mat']; 
    %                        filename = [cell2mat(dataname(testIdx(fileId))) '_' mapsname(mId, 1:mapsL(mId)) '_Duke_LbpTopPatch3.mat']; 

       load(fullfile(featurePath, filename)); 

%        fileHist = []; 
%        for j = 1 : length(Histogram)
%                tem = double(Histogram{j}); 
%                tem = tem'; 
%                fileHist= [fileHist, tem]; 
%        end 

       fileHist = cat(1, Histogram{:}); 
       fileHist = fileHist'; 

       hists{fileId} = getImageDescriptor(model, fileHist);
       test_label = [test_label, label(testIdx(fileId))]; 
    end 
    hists = cat(2, hists{:}) ;

    % --------------------------------------------------------------------
    %    Compute feature map - this step could be removed
    % --------------------------------------------------------------------

    %Test_psix = vl_homkermap(hists, 1, 'kchi2', 'gamma', .5) ;
    %Test_data =  FeatureScale(Test_psix') ; 
    test_data = hists'; 
    test_label = test_label'; 


    %---------------------------------------------------------------------
    %   Training RF 
    %---------------------------------------------------------------------

    TrainModel = classRF_train(train_data, train_label, ntree(1)); 

    %---------------------------------------------------------------------
    %  Testing RF 
    %---------------------------------------------------------------------
    predRF = classRF_predict(test_data, TrainModel);         
    ControlLinear = sign(predRF);

    pred_label(testIdx(1)) = ControlLinear(1); 
    pred_label(testIdx(2)) = ControlLinear(2); 
    pred_label(pred_label ==0) = -1 ; 
    save(fullfile(path_to_save, ['pred_label_' num2str(CV) '_' mapsname(mId, 1:mapsL(mId)) '_' '32_100_result.mat']), 'pred_label'); 
   

