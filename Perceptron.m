% traning set
s = [1 1 1; 1 2 0; 2 -1 -1; 2 0 0; -1 2 -1; -2 1 1; -1 -1 -1; -2 -2 0];
t = [-1 -1; -1 -1; -1 1; -1 1; 1 -1; 1 -1; 1 1; 1 1];
Q = 8;
M = 2;

alpha = 1;
b = [0 0];
w = [0 0; 0 0; 0 0];
theta = 0.1;

function f = bipolar(x,theta)
	if x > theta
		f = 1;
	elseif x < theta * -1
		f = -1;
	else
		f = 0;
	end
end

count = 0;
while count<= Q
	for q = 1:Q % iterate through input vectors
		yin = [0 0];
		y = [0 0];
		fprintf('s(q)=[%d %d %d]\t', s(q,1), s(q,2), s(q,3));
		for j = 1:M % total M decision hyperplates
			yin(j) = s(q,:) * w(:,j) + b(j);
			y(j) = bipolar(s(q,:) * w(:,j) + b(j),theta);
		end
		fprintf('yin=[%d %d]\t y=[%d %d]\t t=[%d %d]\t',yin(1), yin(2), y(1), y(2), t(q,1), t(q,2));
		if isequal(y,t(q,:)) == 0
			for j = 1:M
				w(:,j) += alpha * s(q,:)'* t(q,j);
				b(j) += alpha * t(q,j);
			end
			fprintf('w=[%d %d ;%d %d ;%d %d]\t b=[%d %d]\n', w(1), w(4), w(2), w(5), w(3), w(6), b(1), b(2));
		else
			count += 1;
			fprintf('No Change\n')
		end
	end
end

disp(w)
disp(b)