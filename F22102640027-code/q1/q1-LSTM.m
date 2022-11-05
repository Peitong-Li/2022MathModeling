% ��������
clc; clear;
data = importdata('data.txt');
data = data';
% data = fliplr(data);
figure();
p=plot(data);
xlabel("����");
ylabel("������Ⱦ��");
title("������������Ⱦ��");
p.LineWidth=2;

% ���������ѵ������?
numTimeStepsTrain = 23
disp('ѵ����ʼ���ڣ�3��4��');
disp('ѵ����3��26��');
dataTrain = data(1:numTimeStepsTrain+1);

dataTest = data(numTimeStepsTrain+1:end);
disp('����������ʵֵ��');
disp(dataTest);
% ѵ�����ݹ�һ��?
mu = mean(dataTrain);
sig = std(dataTrain);

dataTrainStandardized = (dataTrain - mu) / sig;

XTrain = dataTrainStandardized(1:end-1);
YTrain = dataTrainStandardized(2:end); 

% ��������ṹ
layers = [
    sequenceInputLayer(1,"Name","input")
    lstmLayer(128,"Name","lstm")
%     dropoutLayer(0.2,"Name","drop")
    fullyConnectedLayer(1,"Name","fc")
    regressionLayer];
% ����ѵ������
%
options = trainingOptions('adam', ...
    'MaxEpochs',400, ...
    'InitialLearnRate',0.005, ...
    'GradientThreshold',1, ...
    'LearnRateSchedule','piecewise', ...
    'LearnRateDropPeriod',125, ...
    'LearnRateDropFactor',0.2, ...
    'Verbose',0, ...
    'Plots','training-progress'); 

% ѵ������
net = trainNetwork(XTrain,YTrain,layers,options); 

% ���Լ���һ��?
dataTestStandardized = (dataTest - mu) / sig;
XTest = dataTestStandardized(1:end-1);
% Ԥ��
net = predictAndUpdateState(net,XTrain);
[net,YPred] = predictAndUpdateState(net,YTrain(end));

numTimeStepsTest = numel(XTest);
for i = 2:numTimeStepsTest
    [net,YPred(:,i)] = predictAndUpdateState(net,YPred(:,i-1),'ExecutionEnvironment','cpu');
    
end 

YPred = sig*YPred + mu; 
disp('���Ի���Ԥ��ֵ��');
disp(YPred);
% ��ͼ
figure
plot(dataTrain(1:end-1))
hold on
idx = numTimeStepsTrain:(numTimeStepsTrain+numTimeStepsTest);
plot(idx,[data(numTimeStepsTrain) YPred],'k.-'),hold on
plot(idx,data(numTimeStepsTrain:end-1),'r'),hold on
hold off
xlabel("����")
ylabel("������Ⱦ������")
title("������3��4����5��1��������Ⱦ��Ԥ�⣨δʹ���߲˰���")
legend(["Observed" "Forecast"]) 