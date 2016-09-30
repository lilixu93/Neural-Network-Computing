s = [1 1; 1 -1; -1 1; -1 -1];
t = [-1 -1 -1 -1];

Q = 4;
M = 2;
alpha = 1;
b = [0 0];
w = [0 0; 0 0];
theta = 0;

function f = bipolar(x,theta)
	if x > theta
		f = 1;
	elseif x < theta * -1
		f = -1;
	else
		f = 0;
	end
end

for ti = 1:3
	for q = 1:Q
		yin = s(q) * w' + b;
		y = bipolar(yin, theta);
		if y ~= t(q)
			w += alpha * s(q) * t(q);
			b += alpha * t(q);
		end
	end
end
disp(w);
disp(b);