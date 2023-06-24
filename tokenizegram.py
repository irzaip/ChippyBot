import tiktoken as tt

aa = tt.get_encoding("gpt2")
aa.encode("Hello aparatus")
aa.decode([9906, 58316, 1015])

