% 导入数据
clc; clear;
data = importdata('data.txt');
data = data';
% data = fliplr(data);
figure();
p=plot(data);
xlabel("天数");
ylabel("新增感染者");
title("长春市新增感染者");
p.LineWidth=2;

% 定义测试与训练长度?
numTimeStepsTrain = 23
disp('训练起始日期：3月4日');
disp('训练到3月26日');
dataTrain = data(1:numTimeStepsTrain+1);

dataTest = data(numTimeStepsTrain+1:end);
disp('测试数据真实值：');
disp(dataTest);
% 训练数据归一化?
mu = mean(dataTrain);
sig = std(dataTrain);

dataTrainStandardized = (dataTrain - mu) / sig;

XTrain = dataTrainStandardized(1:end-1);
YTrain = dataTrainStandardized(2:end); 

% 定义网络结构
layers = [
    sequenceInputLayer(1,"Name","input")
    lstmLayer(128,"Name","lstm")
%     dropoutLayer(0.2,"Name","drop")
    fullyConnectedLayer(1,"Name","fc")
    regressionLayer];
% 定义训练参数
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

% 训练网络
net = trainNetwork(XTrain,YTrain,layers,options); 

% 测试集归一化?
dataTestStandardized = (dataTest - mu) / sig;
XTest = dataTestStandardized(1:end-1);
% 预测
net = predictAndUpdateState(net,XTrain);
[net,YPred] = predictAndUpdateState(net,YTrain(end));

numTimeStepsTest = numel(XTest);
for i = 2:numTimeStepsTest
    [net,YPred(:,i)] = predictAndUpdateState(net,YPred(:,i-1),'ExecutionEnvironment','cpu');
    
end 

YPred = sig*YPred + mu; 
disp('测试机的预测值：');
disp(YPred);
% 绘图
figure
plot(dataTrain(1:end-1))
hold on
idx = numTimeStepsTrain:(numTimeStepsTrain+numTimeStepsTest);
plot(idx,[data(numTimeStepsTrain) YPred],'k.-'),hold on
plot(idx,data(numTimeStepsTrain:end-1),'r'),hold on
hold off
xlabel("天数")
ylabel("新增感染者数量")
title("长春市3月4日起到5月1日新增感染者预测（未使用蔬菜包）")
legend(["Observed" "Forecast"]) 