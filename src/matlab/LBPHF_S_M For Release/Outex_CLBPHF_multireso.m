%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Authors: Guoying Zhao, Timo Ahonen, Jiri Matas & Matti 
%Pietik?inen (2012)
%Rotation-invariant image and video description with local binary %pattern features. IEEE Transactions on Image Processing, 21%(4):1465-1467

% Copyright @ Center for Machine Vision Research, University of %% Oulu, Finland

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% This is an example code how to implement LBPHF_S_M as an %rotation invariant descriptor combining sign and magnitude information with histogram Fourier transform for texture representaion.


clear all;

rootpic = 'Outex_TC_00012\';
% picture number of the database
% picNum = 4320;  % in Outex_TC_00010
picNum = 9120;  % in Outex_TC_00012

% multiresolution 
scales=[
1 0 0
0 1 0
0 0 1
1 1 0
1 0 1
0 1 1
1 1 1 ];

% change currScale to get multiresolution 
currScale = scales(1,:);

patternMapping1u2 = getmapnew(8,'u2');
patternMapping2u2 = getmapnew(16,'u2');
patternMapping3u2 = getmapnew(24,'u2');

LBPHF=[];

tic
for i=1:picNum;
    filename = sprintf('%s\\images\\%06d.ras', rootpic, i-1);
    Gray = imread(filename);
    Gray = double(Gray);
    
    fv1= []; fv2 = []; fv3 = []; fv4 = []; fv5 = []; fv6 = [];
    
    if(currScale(1))
                [CLBP_S,CLBP_M,CLBP_C] = clbp(Gray,1,8,patternMapping1u2,'x');
                % Generate histogram of CLBP_S
                CLBP_SH= hist(CLBP_S(:),0:patternMapping1u2.num-1);

                % Generate histogram of CLBP_M
                CLBP_MH = hist(CLBP_M(:),0:patternMapping1u2.num-1);
 
                % Generate LBPHF_S
                fv1=constructhf(CLBP_SH,patternMapping1u2);

			% Generate LBPHF_M
                fv2=constructhf(CLBP_MH,patternMapping1u2);
 
    end
       
    if(currScale(2))
                [CLBP_S,CLBP_M,CLBP_C] = clbp(Gray,2,16,patternMapping2u2,'x');

                % Generate histogram of CLBP_S
                CLBP_SH= hist(CLBP_S(:),0:patternMapping2u2.num-1);
%                
                % Generate histogram of CLBP_M
                CLBP_MH = hist(CLBP_M(:),0:patternMapping2u2.num-1);
 			% Generate LBPHF_S
                fv3=constructhf(CLBP_SH,patternMapping2u2);

			% Generate LBPHF_M
                fv4=constructhf(CLBP_MH,patternMapping2u2);
 
    end
    
    if(currScale(3))
                [CLBP_S,CLBP_M,CLBP_C] = clbp(Gray,3,24,patternMapping3u2,'x');
                % Generate histogram of CLBP_S
                CLBP_SH= hist(CLBP_S(:),0:patternMapping3u2.num-1);

                % Generate histogram of CLBP_M
                CLBP_MH = hist(CLBP_M(:),0:patternMapping3u2.num-1);
   			% Generate LBPHF_S
                fv5=constructhf(CLBP_SH,patternMapping3u2);

			% Generate LBPHF_M
                fv6=constructhf(CLBP_MH,patternMapping3u2);
                

    end
                
            LBPHF(i,:) = [fv1 fv2 fv3 fv4 fv5 fv6];
       
end
toc

% read picture ID of training and test samples, and read class ID of
% training and test samples
trainTxt = sprintf('%s001\\train.txt', rootpic);
testTxt = sprintf('%s001\\test.txt', rootpic);
[trainIDs, trainClassIDs] = ReadOutexTxt(trainTxt);
[testIDs, testClassIDs] = ReadOutexTxt(testTxt);


 % classification test 
    trains = LBPHF(trainIDs,:);
    tests = LBPHF(testIDs,:);

    trainNum = size(trains,1);
    testNum = size(tests,1);

% use L1 distance as metric measure
    [final_accu,PreLabel] = NNClassifier_L1(trains',tests',trainClassIDs,testClassIDs);
    accu_list3 = final_accu;
    close all;