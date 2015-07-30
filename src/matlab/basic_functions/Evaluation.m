function [Acc, Sensitivity, Specificity, Precision] = Evaluation(Control, LabelTest)

%%%% TPR = Recall , Sensitiviy 
%%%% TNR = specificity 
%%%% Precision

error = sum(Control ~= LabelTest)/length(LabelTest); 
Acc = 1 - error; 
% [CM order] = confusionmat(LabelTest, Control); 
Pos = zeros (size(LabelTest)); 
Neg = zeros(size(LabelTest)); 

Pos (LabelTest == 1) = 1 ; 
Neg (LabelTest == -1) = 1 ; 
D = Control.*LabelTest; 
DPos = D.*Pos; 
DNeg = D.*Neg ; 

TP = sum(DPos == 1); 
TN = sum(DNeg == 1); 

FN = sum(DPos == -1); 
FP = sum(DNeg == -1);

%%% Sensitivity = Recall = TPR = TP/(TP+FN); 
Sensitivity = TP /(TP + FN); 

%%% Specificity  = TNR 
Specificity = TN / (FP + TN); 

%%% Precision 
Precision  = TP / (TP + FP); 

%%% ConfMat 
ConfMat = [TP FP; FN TN]; 
