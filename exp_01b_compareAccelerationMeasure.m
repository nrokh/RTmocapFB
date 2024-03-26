%%%%%%%%%%%%%%%%%%%%%%%%% nrokh 2024 %%%%%%%%%%%%%%%%%%%%%%%%%
% 
% Purpose: Process acc. data collected with GaitGuide
% Dependencies: acc. data in the workspace
% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

subject = 1;                    % subject ID
day = 0;                        % day 0 or 1
filename = 's1_d0_pp';          % target file saving name

%% 1. Load data from workspace 
% e.g. "s1_d0_RIGHT.mat"
load(['s'  num2str(subject) '_d' num2str(day)  '_RIGHT.mat'])
load(['s'  num2str(subject) '_d' num2str(day)  '_LEFT.mat'])

%% 2. Remove early data transients
dataLeft = GG_s1_LEFT(1200:end);    % change this iteratively
dataRight = GG_s1_RIGHT(1200:end);  % dynamic naming is hard in matlab :-(

%% 3. Convert to [g] and filter
% a. convert units 
acc = 16;
scale = 32768 / acc;

dataLeft = dataLeft./scale;
dataRight = dataRight./scale;

% b. apply low-pass filter and plot
Fs = 26667;
Fc    = 200; %cutoff freq
[b,a] = butter(6,Fc/(Fs/2), 'low');
dataLeft_filt    = filtfilt(b, a, dataLeft);
dataRight_filt    = filtfilt(b, a, dataRight);

% iii. plot
subplot(2,1,1)
plot(dataLeft_filt)
subplot(2,1,2)
plot(dataRight_filt)

%% 4. Process into individual chunks

threshold = 0.001;
window_size = 0.150*Fs; 

% a. LEFT
data_region_inds = find(abs(diff(dataLeft_filt))>threshold); % find the data
jumps = find(abs(diff(data_region_inds)) > 100); % these are cutoff indices in the "data_region"
data_region = cell(1,0);
jumps = [1; jumps; length(data_region_inds)];
for i = 1:length(jumps)-1
    data_region{i} = data_region_inds(jumps(i):jumps(i+1));
end
dataSegmentedLeft = cell(1,0);
for i = 1:length(data_region)
    dataSegmentedLeft{i} = dataLeft_filt(round(data_region{i}(2) - window_size) : round(data_region{i}(end) + window_size));
end

% b. LEFT
data_region_inds = find(abs(diff(dataRight_filt))>threshold); % find the data
jumps = find(abs(diff(data_region_inds)) > 100); % these are cutoff indices in the "data_region"
data_region = cell(1,0);
jumps = [1; jumps; length(data_region_inds)];
for i = 1:length(jumps)-1
    data_region{i} = data_region_inds(jumps(i):jumps(i+1));
end
dataSegmentedRight = cell(1,0);
for i = 1:length(data_region)
    dataSegmentedRight{i} = dataRight_filt(round(data_region{i}(2) - window_size) : round(data_region{i}(end) + window_size));
end

%% 5. Visualize
figure; hold on;
title('Left')
for i = 1:length(dataSegmentedLeft)
    plot(dataSegmentedLeft{i})
end

figure; hold on;
title('Right')
for i = 1:length(dataSegmentedRight)
    plot(dataSegmentedRight{i})
end


%% 6. Compute and print peak-to-peak amplitude

for i = 1:length(dataSegmentedLeft)
    ppAmp = mean(maxk(dataSegmentedLeft{i},3) - mink(dataSegmentedLeft{i},3));
    disp(['Left: #' num2str(i) ' = ' num2str(ppAmp)])
end

for i = 1:length(dataSegmentedRight)
    ppAmp = mean(maxk(dataSegmentedRight{i},3) - mink(dataSegmentedRight{i},3));
    disp(['Right: #' num2str(i) ' = ' num2str(ppAmp)])
end