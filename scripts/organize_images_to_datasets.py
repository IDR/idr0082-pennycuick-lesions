#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
#   Copyright (C) 2017 University of Dundee. All rights reserved.
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# ------------------------------------------------------------------------------


"""
This script creates a new dataset and links all images with a given name to it.
"""

import argparse
import omero
import omero.cli
import omero.clients
from omero.gateway import BlitzGateway

project_id = 1052

def run(project_id):
	try:
		conn.connect()
    	for dataset in project.linkedDatasetList():
			if dataset.getName().getValue() == 'goodname'
				for image in dataset.linkedImageList():
					image_name_space = image.getName().getValue().split(' ')
					length = len(image_name_space)
					image_ending_right = (image_name_space[length-1] == '[0]')
					image_name_dot = image.getName().getValue().split('.')
					image_matches_attachment = (att_name_parts[0] == image_name_dot[0])
					if (image_ending_right and image_matches_attachment):
						print("Linked dataset %s to image %s" %
								(image.getName().getValue()))

		dataset = omero.model.DatasetI()
		dataset.setName(omero.rtypes.rstring(dataset_name))
		dataset = conn.getUpdateService().saveAndReturnObject(dataset)
		dataset_id = dataset.getId().getValue()
		print(username, dataset_id)

		link = omero.model.DatasetImageLinkI()
		link.setParent(dataset)
		link.setChild(omero.model.ImageI(image_id, False))
		conn.getUpdateService().saveObject(link)
	except Exception as exc:
		print("Error while linking images: %s" % str(exc))
	finally:
		conn.close()


def main(args):
	cs = conn.getContainerService()
	param = omero.sys.ParametersI().leaves()
	project = cs.loadContainerHierarchy("Project", [project_id], param)[0]
	run


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
	with omero.cli.cli_login() as c:
        conn = omero.gateway.BlitzGateway(client_obj=c.get_client())
        main(conn)
