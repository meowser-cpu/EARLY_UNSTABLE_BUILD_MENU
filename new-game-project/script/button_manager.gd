extends Control

var center: Vector2
@onready var button_manager: Control = $"."
@onready var texture_button: TextureButton = $TextureButton
@onready var options: TextureButton = $Options
@onready var exit: TextureButton = $Exit



func _ready():
	$TextureButton.pos()

	
	center = Vector2(get_viewport_rect().size.x/2, get_viewport_rect().size.y/2)

func _process(_delta):
	var tween = button_manager.create_tween()
	var offset = center - get_global_mouse_position() * 0.1
	tween.tween_property(button_manager,"position",offset,1.0)
