extends Node2D


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.



func _on_texture_button_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/texture_button.tscn")


func _on_options_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/options.tscn")


func _on_exit_pressed() -> void:
	get_tree().quit()
