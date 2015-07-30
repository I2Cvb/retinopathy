%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Feature Sacling 
%%%% Mojdeh Rastgoo , UdG , 5-08-13
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Normalizing features between 1 and -1 with respect to the mean and min
%%% and max of the feature 
%%% FV = [samples , features]
%%% Use min

function FVnorm = FeatureScale(FV , option)
[samples, features] = size(FV); 
 if option == 1  
     %%% Rescaling 
    maxfeatures = max(FV); 
    minfeatures = min(FV); 
    meanfeatures = mean(FV); 
    FVnorm = zeros(samples, features); 

    for i  = 1 : features 
        FVnorm(:,i) = (FV(:,i) - meanfeatures(i))./(maxfeatures(i) - minfeatures(i)); 
        FVnorm(:,i) = removeinf (FVnorm(:,i), 1); 
    end 
 elseif option == 2 
          %%% Rescaling 
     maxfeatures = max(FV); 
     minfeatures = min(FV); 
     FVnorm = zeros(samples, features); 

     for i  = 1 : features 
        FVnorm(:,i) = (FV(:,i) - minfeatures(i))./(maxfeatures(i) - minfeatures(i)); 
        FVnorm(:,i) = removeinf (FVnorm(:,i), 1); 
     end
 elseif option == 0
     %%% L1 norm 
     for i = 1 : samples 
        FVnorm(i,:) = (FV(i,:))./sum(FV(i,:)); 
        FVnorm(i,:) = removeinf(FVnorm(i,:), 1); 
        
     end 
     
 elseif option == 2 
       FVnorm = FV; 
 end 
FVnorm  = removenan(FVnorm); 



