%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% BoF - Mojdeh - Guillaume - Sik - Desire 
%%% OCT images - Two vs all 
%%% UB - 10 - 06 - 15 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    addpath ../../toolbox/vlfeat-0.9.16/toolbox/
    vl_setup
    addpath ../../toolbox/basic_functions/
    addpath ../../toolbox/RF_Class_C/
    

    filePath  = '/media/lemaitre/My Passport/PhD/Coding/OrganizedCode/OCT_processing/'; 
    featurePath = '/media/lemaitre/My Passport/PhD/Coding/OrganizedCode/OCT_processing/features/'; 
    path_to_save = '/media/lemaitre/My Passport/PhD/Coding/OrganizedCode/OCT_processing/result/'; 
    modelPath = '/media/lemaitre/My Passport/PhD/Coding/OrganizedCode/OCT_processing/model/'; 

    data = csv2cell(fullfile(filePath, 'data2.csv'), 'fromfile'); 
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

    pred_label =  zeros(30,1); 


    for CV = 1 : 15
        
        Idx = 1 : 30 ; 
        testIdx = [CV, CV+15]; 
        trainIdx = Idx ; 
        trainIdx(testIdx) =[]; 
        train_label = [];
        modelname1 = ['model3_Duke_'  mapsname(1, 1:mapsL(1)) '_' num2str(numWords(1)) '_' num2str(CV) '.mat']; 
        model1 = load(fullfile(modelPath, modelname1)); 
        modelname2 = ['model3_Duke_'  mapsname(2, 1:mapsL(2)) '_' num2str(numWords(1)) '_' num2str(CV) '.mat']; 
        model2 = load(fullfile(modelPath, modelname2)); 
        modelname3 = ['model3_Duke_'  mapsname(3, 1:mapsL(3)) '_' num2str(numWords(1)) '_' num2str(CV) '.mat']; 
        model3 = load(fullfile(modelPath, modelname3)); 


        % --------------------------------------------------------------------
        %     Compute spatial histograms - Train Set 
        % --------------------------------------------------------------------
        hists1 = {} ;
        hists2 = {};
        hists3 = {}; 

        for fileId = 1 : length(trainIdx)
          
%             filename = [cell2mat(dataname(trainIdx(fileId))) '_nlm_' mapsname(mId, 1:mapsL(mId)) '_LbpTopPatch3.mat']; 
            filename = [cell2mat(dataname(trainIdx(fileId))) '_' mapsname(1, 1:mapsL(1)) '_Duke_LbpTopPatch3.mat']; 
            load(fullfile(featurePath, filename)); 
            fileHist = cat(1, Histogram{:}); 
            fileHist = fileHist'; 
            hists1{fileId} = getImageDescriptor(model1.model, fileHist); clear Histogram; 
            
            filename = [cell2mat(dataname(trainIdx(fileId))) '_' mapsname(2, 1:mapsL(2)) '_Duke_LbpTopPatch3.mat']; 
            load(fullfile(featurePath, filename)); 
            fileHist = cat(1, Histogram{:}); 
            fileHist = fileHist'; 
            hists2{fileId} = getImageDescriptor(model2.model, fileHist); clear Histogram  ; 

            
            filename = [cell2mat(dataname(trainIdx(fileId))) '_' mapsname(3, 1:mapsL(3)) '_Duke_LbpTopPatch3.mat']; 
            load(fullfile(featurePath, filename)); 
            fileHist = cat(1, Histogram{:}); 
            fileHist = fileHist'; 
            hists3{fileId} = getImageDescriptor(model3.model, fileHist); clear Histogram; 


            train_label = [train_label, label(trainIdx(fileId))]; 
        end 
        hists1 = cat(2, hists1{:}) ;
        hists2 = cat(2, hists2{:}) ;
        hists3 = cat(2, hists3{:}) ;


        
        % --------------------------------------------------------------------
        %    Compute feature map - this step could be removed
        % --------------------------------------------------------------------
        train_data = []; 
        train_data = [train_data, hists1', hists2', hists3']; 
        train_label = train_label'; 


        test_label = []; 
        % --------------------------------------------------------------------
        %     Compute spatial histograms - Test Set 
        % --------------------------------------------------------------------
        hists1 = {} ;
        hists2 = {} ;
        hists3 = {} ;

        for fileId = 1 : length(testIdx)

           filename = [cell2mat(dataname(testIdx(fileId))) '_' mapsname(1, 1:mapsL(1)) '_Duke_LbpTopPatch3.mat']; 
           load(fullfile(featurePath, filename)); 
           fileHist = cat(1, Histogram{:}); 
           fileHist = fileHist'; 
           hists1{fileId} = getImageDescriptor(model1.model, fileHist); clear Histogram; 
           
           filename = [cell2mat(dataname(testIdx(fileId))) '_' mapsname(2, 1:mapsL(2)) '_Duke_LbpTopPatch3.mat']; 
           load(fullfile(featurePath, filename)); 
           fileHist = cat(1, Histogram{:}); 
           fileHist = fileHist'; 
           hists2{fileId} = getImageDescriptor(model2.model, fileHist); clear Histogram ; 
           
           filename = [cell2mat(dataname(testIdx(fileId))) '_' mapsname(3, 1:mapsL(3)) '_Duke_LbpTopPatch3.mat']; 
           load(fullfile(featurePath, filename)); 
           fileHist = cat(1, Histogram{:}); 
           fileHist = fileHist'; 
           hists3{fileId} = getImageDescriptor(model3.model, fileHist);
           test_label = [test_label, label(testIdx(fileId))]; 
           
        end 
        hists1 = cat(2, hists1{:}) ;
        hists2 = cat(2, hists2{:}) ;
        hists3 = cat(2, hists3{:}) ;
        % --------------------------------------------------------------------
        %    Compute feature map - this step could be removed
        % --------------------------------------------------------------------

        %Test_psix = vl_homkermap(hists, 1, 'kchi2', 'gamma', .5) ;
        %Test_data =  FeatureScale(Test_psix') ; 
        test_data = []; 
        test_data = [test_data, hists1', hists2', hists3']; 
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


    end
    pred_label(pred_label ==0) = -1 ; 
    label(label==0) = -1 ; 

   [Acc(nId, WId), TPR(nId, WId), TNR(nId, WId), PRE(nId, WId)] = Evaluation(pred_label, label'); 
 
   save(fullfile(path_to_save, ['81624_Duke_32_100_result.mat']), 'Acc', 'TPR', 'TNR', 'PRE'); 
   

