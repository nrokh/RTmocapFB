% nrokh 2023
% exporting data to .csv for python analysis later

% 1. Load metadata
load('C:\Users\rokhmanova\Desktop\winterbreakremoteaccess\retrainingMeta.mat')
dataPath = "C:\Users\rokhmanova\Desktop\winterbreakremoteaccess\02_PP Data_untrimmed\s";

cond_list = ["b","ti"];

% load data
for sub_i = 1:10%:length(retrainingMeta)
    sub = retrainingMeta(sub_i,1);
    
    % i. load baseline and toe-in marker data trials
    if sub<10
        sub_b = load(dataPath + "0" + sub + "\MBLS0" + sub + "walkPostProcessed.mat");
        sub_ti = load(dataPath + "0" + sub + "\MBLS0" + sub + "toeinPostProcessed.mat");
        
        sub_id = "0"+num2str(sub);
    else
        sub_b = load(dataPath +  sub + "\MBLS" + sub + "walkPostProcessed.mat");
        sub_ti = load(dataPath +  sub + "\MBLS" + sub + "toeinPostProcessed.mat");
        
        sub_id = num2str(sub);
    end
    
    % ii. find marker numbers based on data labels
    [leftNums_b, rightNums_b] = findMarkerNums(sub_b.mblMarkerDataStruct);
    [leftNums_ti, rightNums_ti] = findMarkerNums(sub_ti.mblMarkerDataStruct);
    
    disp("Subject " + sub_id + " loaded.")
    for i =1:2
        cond = cond_list(i); %do baseline and toein
        
        % load mblForceDataStruct and mblMarkerDataStruct
        if i == 1
            labels = sub_b.mblMarkerDataStruct.labels;
        else
            labels = sub_ti.mblMarkerDataStruct.labels;
        end
        
        % left leg
        Lcal_num = [ 3*find(matches(labels, 'LCAL'),1)-2, 3*find(matches(labels, 'LCAL'),1)-1, 3*find(matches(labels, 'LCAL'),1)];
        L2mt_num = [ 3*find(matches(labels, 'L2MT'),1)-2, 3*find(matches(labels, 'L2MT'),1)-1, 3*find(matches(labels, 'L2MT'),1)];
        Lmep_num = [ 3*find(matches(labels, 'LMEP'),1)-2, 3*find(matches(labels, 'LMEP'),1)-1, 3*find(matches(labels, 'LMEP'),1)];
        Llep_num = [ 3*find(matches(labels, 'LLEP'),1)-2, 3*find(matches(labels, 'LLEP'),1)-1, 3*find(matches(labels, 'LLEP'),1)];
        Lasi_num = [ 3*find(matches(labels, 'LASI'),1)-2, 3*find(matches(labels, 'LASI'),1)-1, 3*find(matches(labels, 'LASI'),1)];
        Lpsi_num = [ 3*find(matches(labels, 'LPSI'),1)-2, 3*find(matches(labels, 'LPSI'),1)-1, 3*find(matches(labels, 'LPSI'),1)];
        Lgtr_num = [ 3*find(matches(labels, 'LGTR'),1)-2, 3*find(matches(labels, 'LGTR'),1)-1, 3*find(matches(labels, 'LGTR'),1)];
        Llml_num = [ 3*find(matches(labels, 'LLML'),1)-2, 3*find(matches(labels, 'LLML'),1)-1, 3*find(matches(labels, 'LLML'),1)];
        Lmml_num = [ 3*find(matches(labels, 'LMML'),1)-2, 3*find(matches(labels, 'LMML'),1)-1, 3*find(matches(labels, 'LMML'),1)];
        
        
        % right leg
        Rcal_num = [ 3*find(matches(labels, 'RCAL'),1)-2, 3*find(matches(labels, 'RCAL'),1)-1, 3*find(matches(labels, 'RCAL'),1)];
        R2mt_num = [ 3*find(matches(labels, 'R2MT'),1)-2, 3*find(matches(labels, 'R2MT'),1)-1, 3*find(matches(labels, 'R2MT'),1)];
        Rmep_num = [ 3*find(matches(labels, 'RMEP'),1)-2, 3*find(matches(labels, 'RMEP'),1)-1, 3*find(matches(labels, 'RMEP'),1)];
        Rlep_num = [ 3*find(matches(labels, 'RLEP'),1)-2, 3*find(matches(labels, 'RLEP'),1)-1, 3*find(matches(labels, 'RLEP'),1)];
        Rasi_num = [ 3*find(matches(labels, 'RASI'),1)-2, 3*find(matches(labels, 'RASI'),1)-1, 3*find(matches(labels, 'RASI'),1)];
        Rpsi_num = [ 3*find(matches(labels, 'RPSI'),1)-2, 3*find(matches(labels, 'RPSI'),1)-1, 3*find(matches(labels, 'RPSI'),1)];
        Rgtr_num = [ 3*find(matches(labels, 'RGTR'),1)-2, 3*find(matches(labels, 'RGTR'),1)-1, 3*find(matches(labels, 'RGTR'),1)];
        Rlml_num = [ 3*find(matches(labels, 'RLML'),1)-2, 3*find(matches(labels, 'RLML'),1)-1, 3*find(matches(labels, 'RLML'),1)];
        Rmml_num = [ 3*find(matches(labels, 'RMML'),1)-2, 3*find(matches(labels, 'RMML'),1)-1, 3*find(matches(labels, 'RMML'),1)];
        
        
        markerNums = {'LCAL', Lcal_num; 'L2MT', L2mt_num; 'LMEP', Lmep_num; 'LLEP', Llep_num; ...
            'LASI', Lasi_num; 'LPSI', Lpsi_num; 'LGTR', Lgtr_num; 'RCAL', Rcal_num; 'R2MT', ...
            R2mt_num; 'RMEP', Rmep_num; 'RLEP', Rlep_num; 'RASI', Rasi_num; 'RPSI', Rpsi_num; ...
            'RGTR', Rgtr_num; 'LLML', Llml_num; 'LMML', Lmml_num; 'RLML', Rlml_num; 'RMML', Rmml_num};
        
        
        % save cal. sac. toe markers
        if i ==1
            Lcal = sub_b.mblMarkerDataStruct.data(:, markerNums{strcmp(markerNums, 'LCAL'),2}(:));
            Lpsi = sub_b.mblMarkerDataStruct.data(:, markerNums{strcmp(markerNums, 'LPSI'),2}(:));
            Ltoe = sub_b.mblMarkerDataStruct.data(:, markerNums{strcmp(markerNums, 'L2MT'),2}(:));
            
            Rcal = sub_b.mblMarkerDataStruct.data(:, markerNums{strcmp(markerNums, 'RCAL'),2}(:));
            Rpsi = sub_b.mblMarkerDataStruct.data(:, markerNums{strcmp(markerNums, 'RPSI'),2}(:));
            Rtoe = sub_b.mblMarkerDataStruct.data(:, markerNums{strcmp(markerNums, 'R2MT'),2}(:));
            
            % save GRF data
            LGRF = sub_b.mblForceDataStruct.data(:,[1:3]);
            RGRF = sub_b.mblForceDataStruct.data(:,[7:9]);
            
        else
            Lcal = sub_ti.mblMarkerDataStruct.data(:, markerNums{strcmp(markerNums, 'LCAL'),2}(:));
            Lpsi = sub_ti.mblMarkerDataStruct.data(:, markerNums{strcmp(markerNums, 'LPSI'),2}(:));
            Ltoe = sub_ti.mblMarkerDataStruct.data(:, markerNums{strcmp(markerNums, 'L2MT'),2}(:));
            
            Rcal = sub_ti.mblMarkerDataStruct.data(:, markerNums{strcmp(markerNums, 'RCAL'),2}(:));
            Rpsi = sub_ti.mblMarkerDataStruct.data(:, markerNums{strcmp(markerNums, 'RPSI'),2}(:));
            Rtoe = sub_ti.mblMarkerDataStruct.data(:, markerNums{strcmp(markerNums, 'R2MT'),2}(:));
            
            % save GRF data
            LGRF = sub_ti.mblForceDataStruct.data(:,[1:3]);
            RGRF = sub_ti.mblForceDataStruct.data(:,[7:9]);
        end
        
        % save data
        writematrix(Lcal,"s"+sub_id + "\s" + sub_id + "_" + cond + "_Lcal.csv")
        writematrix(Lpsi,"s"+sub_id + "\s" + sub_id + "_" + cond + "_Lpsi.csv")
        writematrix(Ltoe,"s"+sub_id + "\s" + sub_id + "_" + cond + "_Ltoe.csv")
        
        writematrix(Rcal,"s"+sub_id + "\s" + sub_id + "_" + cond + "_Rcal.csv")
        writematrix(Rpsi,"s"+sub_id + "\s" + sub_id + "_" + cond + "_Rpsi.csv")
        writematrix(Rtoe,"s"+sub_id + "\s" + sub_id + "_" + cond + "_Rtoe.csv")
        
        writematrix(LGRF,"s"+sub_id + "\s" + sub_id + "_" + cond + "_LGRF.csv")
        writematrix(RGRF,"s"+sub_id + "\s" + sub_id + "_" + cond + "_RGRF.csv")
        
        disp("Condition " + cond + " for sub " + sub_id + " finished.")
    end
end


