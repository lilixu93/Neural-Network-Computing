%training data
x = [1 1; 1 -1; -1 1; -1 -1];
tr = [-1 1 1 -1];
T = 4;
% sigmoid function f = tanh(x/2)
function f = sig(x)
	f = tanh(x ./ 2);
end
function f1 = dsig(x)
	f1 = (1 - tanh(x ./ 2) .^2) ./2;
end
%initialize weights and bias with random values
w1 = rand(2,2) - 0.5;
w2 = rand(2,1) - 0.5;
b1 = rand(1,2) - 0.5;
b2 = rand(1,1) - 0.5;
L = 2;
alpha = 0.11;
%training process
for iter = 1:20000
	for t = 1:T
		a0 = x(t,:); % 1*2 
		n1 = a0 * w1 + b1; % 1*2 . 2*2 + 1*2 = 1*2
		a1 = sig(n1); % 1*2
		n2 = a1 * w2 + b2; % 1*2 . 2*1 + 1*1 = 1*1
		a2 = sig(n2); % 1*1
		% back propagation
		s2 = (a2 - tr(t)) * dsig(n2); % 1*1
		s1 = [dsig(n1)(1)*w2(1)*s2 dsig(n1)(2)*w2(2)*s2];
		w1 -= alpha * a0' * s1;
		b1 -= alpha * s1; 
		w2 -= alpha * a1' * s2;
		b2 -= alpha * s2;
	end
end
w1
b1
w2
b2
% verification
for t = 1:T
	sig(sig(x(t,:)*w1+b1)*w2+b2)
end
