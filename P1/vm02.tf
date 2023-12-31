# https://github.com/garutilorenzo/oracle-cloud-terraform-examples/blob/master/simple-instance/files/oci-ubuntu-install.sh
# https://github.com/garutilorenzo/oracle-cloud-terraform-examples/blob/master/simple-instance/compute.tf

data "cloudinit_config" "vm02" {
  gzip          = true
  base64_encode = true

  part {
    content_type = "text/x-shellscript"
    content      = templatefile("${path.module}/templates/vm02.sh", {})
  }
}

resource "oci_core_instance" "vm02" {
    availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
    compartment_id = var.compartment_id
    display_name = "vm02"
    shape = "VM.Standard3.Flex"
    shape_config {
        memory_in_gbs = "4"
        ocpus         = "1"
    }
    source_details {
        source_type = "image"
        source_id = var.os_image_id
    }
    create_vnic_details {
        subnet_id = oci_core_subnet.public.id
        assign_public_ip = true
    }
    freeform_tags = {
        "Name" = "vm02"
    }
    metadata = {
        ssh_authorized_keys = file("ssh/db2.pub")
        user_data           = data.cloudinit_config.vm02.rendered
    }
    preserve_boot_volume = false

    depends_on = [oci_core_instance.vm01]

}

output "vm02_connect" {
  value = "ssh -i ssh/db2 ubuntu@${oci_core_instance.vm02.public_ip}"
}
