
mode = 'Supervisey';

backOff = IFS;

figName = 'xx';
switch accessCategory
    case 0
        figName = 'vo';
    case 1
        figName = 'vi';
    case 2
        figName = 'be';
    case 3
        figName = 'bg';
end
%
disp(['## ' figName ' #############################']);
disp(['- Found ', num2str(length(locs(:,1))), ' packets, ' num2str(length(IFS)) ' IFSs']);

AIFS = 0;
switch accessCategory
    case 0 % vioce
        AIFS = 34;
    case 1 % video
        AIFS = 34;
    case 2 % BestEffort
        AIFS = 43;
    case 3 % Background
        AIFS = 79;
end

SIFSD = backOff(backOff <= 20.5); 

%%%% Slilance Periods Data
CorrectBackOff = backOff(backOff > 27); % 27 uSec, Guido's recommendation

minBackOff = min(backOff)
textf = [num2str(floor(length(backOff)/2)) ' Samples']; % No of data packets is half the total (no RTS/CTS)
gtitle = ['X Histogram, Data silent periods, ' textf];
xlab = 'time (uSec)';
histScales(2, backOff, 100, gtitle, xlab, 1, [0 min(ceil(max(backOff)), 250)]);
saveas(gcf,['b_' figName '.jpg'])

%%%% Compliance Calculator 
[Bins, prob , probMax, TxopDurations] = EN_301_893_ReqCalc(IFS, locs/sampRate * 1e6, accessCategory, mode);

meanTxop = mean(TxopDurations)
maxTxop = max(TxopDurations)

[SIFSFactor, TxopFactor, AGFactor, KBL, NF] = ComplianceMetric_v101(IFS, SIFSD, locs/sampRate * 1e6, accessCategory, mode);
name = 'GOOGLE';

%dlmwrite('output.csv',name,'-append')
output = {accessCategory, length(IFS), maxTxop, sum(prob > probMax), TxopFactor, AGFactor, KBL, 1 - exp(KBL), SIFSFactor, NF};
dlmwrite('output.csv',output,'-append')


