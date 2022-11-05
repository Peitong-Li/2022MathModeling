clc;clear all;close all;
%% 数据
load './data/chaoyang'

X1=chaoyang;
X=X1(:,2:3);
A = X;
% 观察数据距离，估计epsilon
[index,Dist] = knnsearch(A(2:end,:),A(1,:));
Kdist(1) = Dist;
for i = 1:size(A,1)
    [index,Dist] = knnsearch(A([1:i-1,i+1:end],:),A(i,:));
    Kdist(i) = Dist;
end
sortKdist = sort(Kdist,'descend');
distX = 1:size(A);
plot(distX,sortKdist,'r+-');
grid on;
% 运行DBSCAN
% parament1
epsilon = 0.35;
minPts = 2;
[IDC,isnoise] = DBSCAN(epsilon,minPts,A);
PlotClusterinResult(A,IDC,epsilon,minPts);
% parament2
epsilon= 0.40 ;
minPts=  3   ;
[IDC2,isnoise2] = DBSCAN(epsilon,minPts,A);
PlotClusterinResult(A,IDC2,epsilon,minPts);


function [IDC,isnoise] = DBSCAN(epsilon,minPts,X)
% DBSCAN
    C = 0;
    D = pdist2(X,X);                    % 各元素之间距离
    IDC = zeros(size(X,1),1);
    visited = false(size(X,1),1);       % 访问标志
    isnoise = false(size(X,1),1);       % 噪声
    for i = 1:size(X,1)
        if ~visited(i)
            visited(i) = true;
            Neighbors = find(D(i,:)<=epsilon);      % 找领域样本
            if numel(Neighbors)<minPts
                isnoise(i) = true;
            else
                C = C + 1;
                [IDC,isnoise] = expandCluster(i,Neighbors,C,IDC,isnoise);   % 以核心对象X(j)扩展簇
            end
        end
    end
    
    function [IDC,isnoise] = expandCluster(i,Neighbors,C,IDC,isnoise)
        % 针对核心对象X(i)进行扩展
        IDC(i) = C;         % 将X(j)的领域元素规定为族C
        k = 1;
        while true
            j = Neighbors(k); 
            
            if ~visited(j)
                % 针对未访问元素继续寻找领域样本
                visited(j) = true;
                Neighbors2 = find(D(j,:)<=epsilon);
                if numel(Neighbors2) >= minPts
                    Neighbors = [Neighbors,Neighbors2]; % X(j)也是核心对象
                end
                
            end
            IDC(j) = C;     % 
            k = k +1;
            if k > numel(Neighbors)
                break;
            end
            
        end
    end
end

function PlotClusterinResult(X, IDC,epsilon,minPts)
    figure;
    k=max(IDC);
    Colors=hsv(k);
    Legends = {};
    for i=0:k
        Xi=X(IDC==i,:);
        if i~=0
            Style = 'x';
            MarkerSize = 8;
            Color = Colors(i,:);
            Legends{end+1} = ['Cluster #' num2str(i)];
        else
            Style = 'o';
            MarkerSize = 6;
            Color = [0 0 0];
            if ~isempty(Xi)
                Legends{end+1} = 'Noise';
            end
        end
        if ~isempty(Xi)
            plot(Xi(:,1),Xi(:,2),Style,'MarkerSize',MarkerSize,'Color',Color);
        end
        hold on;
    end
    hold off;
    axis equal;
    grid on;
    legend(Legends);
    legend('Location', 'NorthEastOutside');
    title(['DBSCAN Clustering (\epsilon = ' num2str(epsilon) ', MinPts = ' num2str(minPts) ')']);
end

