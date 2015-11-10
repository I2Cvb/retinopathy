%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% OCT - LBPTOP feature extraction 
%%% Mojdeh - Guillaume - Desire - Joan 
%%% UB - 8-06-15
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function FeatureExtraction_TopLBP_flatten_aligned(aaaa)

addpath ./STLBP_Matlab/
addpath ./basic_functions/
mapPath = '/user1/le2i/gu5306le/Work/OCT_processing/toolbox/STLBP_Matlab/maps/'; 
 Maps = char('8_RIU.mat', '16_RIU.mat', '24_RIU.mat'); 
 MapsLength = [9 10 10]; 
dataPath = '/fhgfs/data/work/le2i/gu5306le/retinopathy/OCT/SERI/pre_processed_data/flatten_aligned_mat/'; 
resPath = '/fhgfs/data/work/le2i/gu5306le/retinopathy/OCT/SERI/feature_data/flatten_aligned/lbp_riu/lbp_hist_top/lbp_global/';


mapsname = char ('8ru', '16ru', '24ru');
mapsnameL = [3 4 4]; 
List = dir (dataPath); 
List = List(3:end);

disp(length(List))

for mId =  2 : 3
    load(fullfile(mapPath, Maps(mId,1:MapsLength(mId))));
    resultPath =  fullfile(resPath, ['r_' num2str(mId) '_hist_mat']);
    %poolobj = parpool('local', 8)
    

    for fileId = 1 : length(List)
        % if fileId <= length(List)
            VolData =  load(fullfile(dataPath, List(fileId).name));
            VolData = VolData.vol_flatten;
            CurrVolData = zeros(size(VolData,1), size(VolData,3), size(VolData,2)); 
            for i = 1 : size(VolData,2)
                CurrVolData(:,:,i) = reshape(VolData(:,i,:), [size(VolData,1) size(VolData,3)]); 
            end
            %end
         
         bBilinearInterpolation = 0;
         TInterval = 1 ; 
         H(fileId).Histogram = LBPTOP(CurrVolData, FxRadius, FyRadius, TInterval, NeighborPoints, TimeLength, BorderLength, bBilinearInterpolation, Bincount, Code);
        
    end
    %delete(poolobj)
    
    for fileId = 1 : length(List)
	Volname = List(fileId).name; 
        Volname = Volname(1:end-4);
        his = H(fileId).Histogram; 
        Histogram = [];
        Histogram = [Histogram, his(1,:), his(2,:), his(3,:)]; 
        save(fullfile(resultPath, [Volname '_lbptop_' num2str(mId) '_hist.mat']) , 'Histogram');
    end 
        
  
    end 
