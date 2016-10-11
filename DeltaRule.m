
% traning set
s = [1 1 1; 1 2 0; 2 -1 -1; 2 0 0; -1 2 -1; -2 1 1; -1 -1 -1; -2 -2 0];
t = [-1 -1; -1 -1; -1 1; -1 1; 1 -1; 1 -1; 1 1; 1 1];
Q = 8;
M = 2;
%initialize
b = [0 0];
w = [0 0; 0 0;0 0];

for k = 1:5000
	alpha = 1/k;
	for q = 1:Q % iterate through input vectors
		y = s(q,:) * w + b;
		w = w - 2 * alpha * s(q,:)'* (y - t(q,:));
		b = b - 2 * alpha * (y - t(q,:));
	end
end

w
b

function y = transfer(yin)
	if yin >=0
		y = 1;
	else
		y = -1;
	end
end

%calculate rms_error
rms = 0;
for q = 1:Q
	yin = s(q,:) * w + b;
	for j = 1:M
		y(j) = transfer(yin(j));
		rms += (yin(j) - t(q,j)) .^ 2;
	end
	fprintf('y=[%d %d] \tt=[%d %d]\n', y(1), y(2), t(q,1), t(q,2));
end
rms /= Q;
rms