CC := gcc
FLAGS := -std=c99 -Wall -Werror
OUT := c.out s.out

run: $(OUT)
	# @clear
	@gnome-terminal --window-with-profile=xs -- zsh -c "./s.out; exec zsh"
	@gnome-terminal --window-with-profile=xs -- zsh -c "./c.out; exec zsh"
	# @gnome-terminal --window-with-profile=xs -- zsh -c "./c.out; exec zsh"
	# @ss -tulpan | grep 'Netid\|s.out'
	# @echo
	# @ss -tulpan | grep 'Netid\|c.out'

c.out: client.c
	$(CC) -o $@ $<

s.out: server.c
	$(CC) -o $@ $<

clean:
	@rm *.out
