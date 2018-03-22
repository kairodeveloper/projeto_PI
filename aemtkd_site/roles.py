from rolepermissions.roles import AbstractUserRole


class Usuario_aluno(AbstractUserRole):
    available_permissions = {
        'create_noticia_record': False,
        'create_evento_record' : False,
        'create_comment_record': True,
        'create_perfil_record' : False,
        'drop_tables': False
    }


class Usuario_administrador(AbstractUserRole):
    available_permissions = {
        'create_noticia_record': True,
        'create_evento_record': True,
        'create_comment_record': True,
        'create_perfil_record': True,
        'drop_tables': True
    }
