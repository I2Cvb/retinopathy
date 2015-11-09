%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% OCT - LBPTOP feature extraction 
%%% Mojdeh - Guillaume - Desire - Joan 
%%% UB - 8-06-15
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function FeatureExtraction_TopLBPPatch(aaaaaaaa)

addpath ./STLBP_Matlab/
addpath ./basic_functions/
mapPath = '/user1/le2i/gu5306le/Work/OCT_processing/toolbox/STLBP_Matlab/maps'; 
Maps = char('8_RIU.mat', '16_RIU.mat', '24_RIU.mat'); 
MapsLength = [9 10 10]; 
dataPath = '/fhgfs/data/work/le2i/gu5306le/retinopathy/OCT/SERI/pre_processed_data/flatten_aligned_mat/'; 
resPath = '/fhgfs/data/work/le2i/gu5306le/retinopathy/OCT/SERI/feature_data/flatten_aligned/lbp_riu/lbp_hist_top/lbp_local/'; 

mapsname = char ('8ru', '16ru', '24ru');
mapsnameL = [3 4 4]; 
List = dir (dataPath); 
List = List(3:end); 


List = dir (dataPath); 
List = List(3:end);

%%% Dividing to 16 * 16 pixels patches 
%ystrIdx = 1:16:128; 
%yendIdx = 16:16:128; 
%xstrIdx = 1:16:512; 
%xendIdx = 16:16:512;
%zstrIdx = 1:16:1024; 
%zendIdx = 16:16:1024; 
%[X, Z,Y] = meshgrid(1:32, 1:64, 1:8); 
%X = X(:) ; Z = Z(:); Y= Y(:);
for mId =  1 : 3
    load(fullfile(mapPath, Maps(mId,1:MapsLength(mId)))); 
    resultPath = fullfile(resPath, ['r_' num2str(mId) '_hist_mat']); 
    %poolobj= parpool('local', 20)
    for fileId = 1 : length(List)
        VolData =  load(fullfile(dataPath, List(fileId).name));
        VolData = VolData.vol_flatten; 
        CurrVolData = zeros(size(VolData,1), size(VolData,3), size(VolData,2)); 
        for i = 1 : size(VolData,2)
            CurrVolData(:,:,i) = reshape(VolData(:,i,:), [size(VolData,1) size(VolData,3)]); 
        end

        ystrIdx = 1:7:size(CurrVolData, 3);
        if rem(size(CurrVolData, 3), 7) ~= 0
            ystrIdx(end) = [];
        end
        yendIdx = 7:7:size(CurrVolData, 3);
        xstrIdx = 1:7:size(CurrVolData, 1);
        if rem(size(CurrVolData, 1) , 7) ~= 0
            xstrIdx(end) = [];
        end
        xendIdx = 7:7:size(CurrVolData, 1);
        zstrIdx = 1:7:size(CurrVolData, 2);
        if rem(size(CurrVolData, 2), 7) ~= 0
            zstrIdx(end) = [];
        end
        zendIdx = 7:7:size(CurrVolData, 2);
        [X, Z, Y] = meshgrid(1: length(xendIdx), 1:length(zendIdx), 1:length(yendIdx));
        X = X(:) ; Z = Z(:); Y = Y(:); 

        for pId = 1 : length(X)
		    PVolume = CurrVolData(xstrIdx(X(pId)):xendIdx(X(pId)),zstrIdx(Z(pId)):zendIdx(Z(pId)) , ystrIdx(Y(pId)):yendIdx(Y(pId))); 
           bBilinearInterpolation = 0;
           histemp = LBPTOP(PVolume, FxRadius, FyRadius, TInterval, NeighborPoints, TimeLength, BorderLength, bBilinearInterpolation, Bincount, Code);
           His = [];
           His = [His, histemp(1,:), histemp(2,:), histemp(3,:)];
H(fileId).Histogram{pId} = His; 
        end

        
     end
        %delete(poolobj)
     for fileId = 1 : length(List)
        Volname = List(fileId).name;
        Volname = Volname(1:end-4);  
        Histogram  = H(fileId).Histogram; 
        save(fullfile(resultPath, [Volname '_lbptopPatch_' num2str(mId) '_.mat']) , 'Histogram');
     end 
        
  
end 
