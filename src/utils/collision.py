def check_collision(entity1, entity2):
    return (entity1.x < entity2.x + entity2.size and
            entity1.x + entity1.size > entity2.x and
            entity1.y < entity2.y + entity2.size and
            entity1.y + entity1.size > entity2.y)