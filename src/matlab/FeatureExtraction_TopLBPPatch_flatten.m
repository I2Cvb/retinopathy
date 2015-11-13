%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% OCT - LBPTOP feature extraction 
%%% Mojdeh - Guillaume - Desire - Joan 
%%% UB - 8-06-15
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function FeatureExtraction_TopLBPPatch_flatten(aaaaaaaa)

addpath ./STLBP_Matlab/
addpath ./basic_functions/
mapPath = '/user1/le2i/gu5306le/Work/OCT_processing/toolbox/STLBP_Matlab/maps'; 
Maps = char('8_RIU.mat', '16_RIU.mat', '24_RIU.mat'); 
MapsLength = [9 10 10]; 
dataPath = '/fhgfs/data/work/le2i/gu5306le/retinopathy/OCT/SERI/pre_processed_data/flatten_mat/'; 
resPath = '/fhgfs/data/work/le2i/gu5306le/retinopathy/OCT/SERI/feature_data/flatten/lbp_riu/lbp_hist_top/lbp_local/'; 

mapsname = char ('8ru', '16ru', '24ru');
mapsnameL = [3 4 4]; 
List = dir (dataPath); 
List = List(3:end); 


List = dir (dataPath); 
List = List(3:end);
overlap = [1 2 3];
w = [9 11 13];


for mId =  3 : 3
    load(fullfile(mapPath, Maps(mId,1:MapsLength(mId)))); 
    resultPath = fullfile(resPath, ['r_' num2str(mId) '_hist_mat']); 

    for fileId = 9:9 %1 : length(List)
        VolData =  load(fullfile(dataPath, List(fileId).name));
        VolData = VolData.vol_flatten; 
        CurrVolData = zeros(size(VolData,1), size(VolData,3), size(VolData,2)); 
        CurrVolData = zeros(size(VolData,1), size(VolData,3), size(VolData,2));
        CurrVolDataPad = zeros(size(VolData,1)+2*overlap(mId), size(VolData,3)+2*overlap(mId), size(VolData,2)+2*overlap(mId));

        for i = 1 : size(VolData,2)
         CurrVolData(:,:,i) = reshape(VolData(:,i,:), [size(VolData,1) size(VolData,3)]);
          % Padding the volume to be able to
          % get the right number of
          % pixels per histogram
          CurrVolDataPad(:,:,i+1) =  padarray(CurrVolData(:,:,i), [overlap(mId) overlap(mId)], 'replicate');
        end
        % The first and last slice of the volume are
        % repeated twice
        CurrVolDataPad(:,:,1) = CurrVolDataPad(:,:,2);
        CurrVolDataPad(:,:,end) =  CurrVolDataPad(:,:,end-1);

         % the window size for each radius of
         % LBP
         % The windows are calculated on th Pad Volume
         n = w(mId);
         ystrIdx = 1:n:size(CurrVolDataPad, 3);
          if rem(size(CurrVolDataPad, 3), n) ~= 0
              ystrIdx(end) = [];
          end
         yendIdx =  n:n: size(CurrVolDataPad, 3);
         xstrIdx =  1: n: size(CurrVolDataPad, 1);
         if rem(size(CurrVolDataPad, 1) , n) ~= 0
                  xstrIdx(end) = [];
          end
         xendIdx = n:n:size(CurrVolDataPad, 1);
         zstrIdx = 1:n:size(CurrVolDataPad, 2);
          if rem(size(CurrVolDataPad, 2), n) ~= 0
                zstrIdx(end) = [];
          end 
         zendIdx = n:n:size(CurrVolDataPad, 2);
         [X, Z, Y] = meshgrid(1: length(xendIdx), 1:length(zendIdx), 1:length(yendIdx));
         X = X(:) ; Z = Z(:); Y = Y(:);
         xstrIdx(2:end) = xstrIdx(2:end)-(2*overlap(mId));
         ystrIdx(2:end) = ystrIdx(2:end)-(2*overlap(mId));
         zstrIdx(2:end) = zstrIdx(2:end)-(2*overlap(mId)); 
         for pId = 1 : length(X)
             
		    PVolume = CurrVolDataPad(xstrIdx(X(pId)):xendIdx(X(pId)),zstrIdx(Z(pId)):zendIdx(Z(pId)) , ystrIdx(Y(pId)):yendIdx(Y(pId))); 
                    bBilinearInterpolation = 0;
                    TInterval = 1;
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
