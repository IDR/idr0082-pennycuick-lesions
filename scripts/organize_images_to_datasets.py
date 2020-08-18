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
This script goes through the Dataset with name "Lung Carcinoma" and sorts out the images from there and unlinks them and relinks them to two new Datasets.
"""

import argparse
import omero
import omero.cli
import omero.clients
from omero.gateway import BlitzGateway

project_id = 1251
dataset_names = ['Lung Carcinoma Overview', 'Lung Carcinoma Overview Mask']

def sortout(project, conn):
    for dataset in project.linkedDatasetList():
        if (dataset.getName().getValue() == 'Lung Carcinoma'):
            for image in dataset.linkedImageList():
                image_name_space = image.getName().getValue().split(' ')
                length = len(image_name_space)
                image_ending_overview = (image_name_space[length-1] == 'image]')
                print (image_name_space[length-1])
                image_ending_mask = (image_name_space[length-2] == 'mask')
                if (image_ending_overview):
                    if (image_ending_mask):
                        print("image %s goes to mask dataset" %
                                (image.getName().getValue()))
                        dataset_name = 'Lung Carcinoma Overview Mask'
                        unlink(image)
                        link_dataset(project, dataset_name, image)
                    else:
                        print("image %s goes to overview dataset" %
                                (image.getName().getValue()))
                        dataset_name = 'Lung Carcinoma Overview'
                        unlink(image)
                        link_dataset(project, dataset_name, image)

def create_datasets(project):
    for dataset_name in dataset_names:
        dataset = omero.model.DatasetI()
        dataset.setName(omero.rtypes.rstring(dataset_name))
        dataset = conn.getUpdateService().saveAndReturnObject(dataset)
        dataset_id = dataset.getId().getValue()
        link = omero.model.ProjectDatasetLinkI()
        link.setParent(omero.model.ProjectI(project.getId(), False))
        link.setChild(omero.model.DatasetI(dataset.getId(), False))
        conn.getUpdateService().saveObject(link)

def unlink(image):
    params = omero.sys.ParametersI()
    params.add('id', image.getId())
    query = "from DatasetImageLink as l where l.child.id=:id"
    query_service = conn.getQueryService()
    link = query_service.findAllByQuery(query, params,
                                                  conn.SERVICE_OPTS)
    print (link[0].getId().getValue())
    links_ids = [link[0].getId().getValue()]
    conn.deleteObjects('DatasetImageLink', links_ids, wait=True)


def link_dataset(project, dataset_name, image):
    for dataset in project.linkedDatasetList():
        print (dataset.getName().getValue())
        print (dataset_name)
        if (dataset.getName().getValue() == dataset_name):
            print ("linking")
            link = omero.model.DatasetImageLinkI()
            link.setParent(omero.model.DatasetI(dataset.getId(), False))
            link.setChild(omero.model.ImageI(image.getId(), False))
            conn.getUpdateService().saveObject(link)



def main(conn):
    cs = conn.getContainerService()
    param = omero.sys.ParametersI().leaves()
    project = cs.loadContainerHierarchy("Project", [project_id], param)[0]
    create_datasets(project)
    project = cs.loadContainerHierarchy("Project", [project_id], param)[0]
    sortout(project, conn)
    conn.close()


if __name__ == '__main__':
    with omero.cli.cli_login() as c:
        conn = omero.gateway.BlitzGateway(client_obj=c.get_client())
        main(conn)
