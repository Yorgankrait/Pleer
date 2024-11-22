import pygame
import os
from typing import List, Dict
from tkinter import filedialog
import tkinter as tk

class Track:
    def __init__(self, title: str, path: str):
        self.title = title
        self.path = path

    def __str__(self):
        return self.title

class Collection:
    def __init__(self, name: str):
        self.name = name
        self.tracks: List[Track] = []

    def add_track(self, track: Track):
        self.tracks.append(track)
        print(f"Трек '{track.title}' добавлен в коллекцию '{self.name}'")

    def remove_track(self, track: Track):
        if track in self.tracks:
            self.tracks.remove(track)
            print(f"Трек '{track.title}' удален из коллекции '{self.name}'")

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.tracks: List[Track] = []
        self.collections: Dict[str, Collection] = {}
        self.current_track_index = 0
        self.is_playing = False

    def add_track(self, title: str, path: str):
        if os.path.exists(path):
            track = Track(title, path)
            self.tracks.append(track)
            print(f"Трек '{title}' добавлен в плеер")
        else:
            print(f"Файл '{path}' не найден")

    def create_collection(self, name: str):
        if name not in self.collections:
            self.collections[name] = Collection(name)
            print(f"Коллекция '{name}' создана")
        else:
            print(f"Коллекция '{name}' уже существует")

    def add_to_collection(self, track_title: str, collection_name: str):
        if collection_name in self.collections:
            track = next((t for t in self.tracks if t.title == track_title), None)
            if track:
                self.collections[collection_name].add_track(track)
            else:
                print(f"Трек '{track_title}' не найден")
        else:
            print(f"Коллекция '{collection_name}' не найдена")

    def play(self):
        if self.tracks:
            pygame.mixer.music.load(self.tracks[self.current_track_index].path)
            pygame.mixer.music.play()
            self.is_playing = True
            print(f"Играет: {self.tracks[self.current_track_index].title}")
        else:
            print("Нет доступных треков")

    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            print("Пауза")
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
            print("Воспроизведение")

    def next_track(self):
        if self.tracks:
            self.current_track_index = (self.current_track_index + 1) % len(self.tracks)
            self.play()

    def previous_track(self):
        if self.tracks:
            self.current_track_index = (self.current_track_index - 1) % len(self.tracks)
            self.play()

    def list_tracks(self):
        if not self.tracks:
            print("Нет доступных треков")
            return
        print("\nСписок треков:")
        for i, track in enumerate(self.tracks, 1):
            print(f"{i}. {track.title}")

    def list_collections(self):
        if not self.collections:
            print("Нет доступных коллекций")
            return
        print("\nСписок коллекций:")
        for name, collection in self.collections.items():
            print(f"\nКоллекция '{name}':")
            for track in collection.tracks:
                print(f"- {track.title}")

def main():
    player = MusicPlayer()
    root = tk.Tk()
    root.withdraw()
    
    while True:
        print("\nВыберите действие:")
        print("1. Добавить трек вручную")
        print("2. Добавить треки через проводник")
        print("3. Воспроизвести/Пауза")
        print("4. Следующий трек")
        print("5. Предыдущий трек")
        print("6. Показать все треки")
        print("7. Создать коллекцию")
        print("8. Добавить трек в коллекцию")
        print("9. Показать коллекции")
        print("10. Выход")

        choice = input("Ваш выбор: ")

        if choice == '1':
            title = input("Введите название трека: ")
            path = input("Введите путь к файлу: ")
            player.add_track(title, path)
        elif choice == '2':
            files = filedialog.askopenfilenames(
                title="Выберите музыкальные файлы",
                filetypes=[
                    ("Аудио файлы", "*.mp3 *.wav *.ogg"),
                    ("Все файлы", "*.*")
                ]
            )
            for file_path in files:
                title = os.path.splitext(os.path.basename(file_path))[0]
                player.add_track(title, file_path)
        elif choice == '3':
            player.pause() if player.is_playing else player.play()
        elif choice == '4':
            player.next_track()
        elif choice == '5':
            player.previous_track()
        elif choice == '6':
            player.list_tracks()
        elif choice == '7':
            name = input("Введите название коллекции: ")
            player.create_collection(name)
        elif choice == '8':
            track_title = input("Введите название трека: ")
            collection_name = input("Введите название коллекции: ")
            player.add_to_collection(track_title, collection_name)
        elif choice == '9':
            player.list_collections()
        elif choice == '10':
            print("Выход из программы")
            pygame.mixer.quit()
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main() 