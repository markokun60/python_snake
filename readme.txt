Create env
py -m venv env_games

activate env
env_games\Scripts\Activate.bat

install
pip install pygame-ce
#pip install pygame-menu-ce

pip install torch torchvision
pip install matplotlib ipython

pip install pyinstaller

create folder 
	data


--------------
pyinstaller --name pySnake  --onedir  -w --icon=snake.ico --add-data "assets:assets" --add-data "resources:resources"  --upx-dir c:/tools/upx  main.py  
pyinstaller --name pySnake  --onefile -w --icon=snake.ico --add-data "assets:assets" --add-data "resources:resources"  --upx-dir c:/tools/upx  main.py  




	https://www.youtube.com/watch?v=ymVdjeufD94&list=PLsFyHm8kJsx32EFcsJNt5sDI_nKsanRUu&index=26

	Reinforcement Learning 
	https://www.youtube.com/watch?v=L8ypSXwyBds&t=89s

https://github.com/patrickloeber/snake-ai-pytorch


https://medium.com/@nancy.q.zhou/teaching-an-ai-to-play-the-snake-game-using-reinforcement-learning-6d2a6e8f3b1c

https://github.com/giaco91/Q-learning-for-snake/blob/main/snake_simple_utils.py
