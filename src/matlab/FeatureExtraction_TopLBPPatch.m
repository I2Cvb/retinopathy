%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% OCT - LBPTOP feature extraction 
%%% Mojdeh - Guillaume - Desire - Joan 
%%% UB - 8-06-15
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
addpath ../../toolbox/STLBP_Matlab/
mapPath = '/user1/le2i/gu5306le/Work/OCT_processing/toolbox/STLBP_Matlab/maps'; 
Maps = char('8_RIU.mat', '16_RIU.mat', '24_RIU.mat'); 
MapsLength = [9 10 10]; 
dataPath = '/fhgfs/data/work/le2i/gu5306le/OCT/nlm_data_mat/'; 
resPath = '/user1/le2i/gu5306le/Work/OCT_processing/result/'; 

mapsname = char ('8ru', '16ru', '24ru');
mapsnameL = [3 4 4]; 
List = dir (dataPath); 
List = List(3:end); 


List = dir (dataPath); 
List = List(3:end); 
%%% Dividing to 16 * 16 pixels patches 
 ystrIdx = 1:16:128; 
 yendIdx = 16:16:128; 
xstrIdx = 1:16:512; 
xendIdx = 16:16:512;
zstrIdx = 1:16:1024; 
zendIdx = 16:16:1024; 
[X, Z,Y] = meshgrid(1:32, 1:64, 1:8); 
X = X(:) ; Z = Z(:); Y= Y(:);
for mId =  1 : 2
    load(fullfile(mapPath, Maps(mId,1:MapsLength(mId)))); 
poolobj= parpool('local', 20)
    parfor fileId = 1 : length(List)
        VolData =  load(fullfile(dataPath, List(fileId).name));
        VolData = VolData.vol_denoised; 
        CurrVolData = zeros(size(VolData,1), size(VolData,3), size(VolData,2)); 
        for i = 1 : size(VolData,2)
            CurrVolData(:,:,i) = reshape(VolData(:,i,:), [size(VolData,1) size(VolData,3)]); 
        end 
        for pId = 1 : length(X)
		    PVolume = CurrVolData(xstrIdx(X(pId)):xendIdx(X(pId)),zstrIdx(Z(pId)):zendIdx(Z(pId)) , ystrIdx(Y(pId)):yendIdx(Y(pId))); 
           bBilinearInterpolation = 0;
            H(fileId).Histogram{pId} = LBPTOP(PVolume, FxRadius, FyRadius, TInterval, NeighborPoints, TimeLength, BorderLength, bBilinearInterpolation, Bincount, Code);
             
        end
        
        
       
        
    end
	delete(poolobj)
    for fileId = 1 : length(List)
        Volname = List(fileId).name;
        Volname = Volname(1:end-4);  
        Histogram  = H(fileId).Histogram; 
        save(fullfile(resPath, [Volname '_' mapsname(mId, 1 : mapsnameL(mId)) '_LbpTopPatch2.mat']) , 'Histogram');
    end 
        
  
end 
