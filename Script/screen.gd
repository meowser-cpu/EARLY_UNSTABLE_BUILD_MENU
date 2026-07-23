extends Control
var center : Vector2
@onready var node = $Control2
func _ready():
	center = Vector2(get_viewport_rect().size.x/2.1, get_viewport_rect().size.y/2.1)
func _process(_delta):
	var tween = node.create_tween()
	var offset = center - get_global_mouse_position() * 0.007
	tween.tween_property(node, "position" ,offset,1.0)


func _on_item_rect_changed():
	center = Vector2(get_viewport_rect().size.x/2.1, get_viewport_rect().size.y/2.1)
	if node!= null:
		node.global_position=center
