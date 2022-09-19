using System.ComponentModel.DataAnnotations;

namespace Divar.Data.Models
{
    public class VisitHistory
    {
        [Key]
        public int Id { get; set; }

        [Display(Name = "تاریخ بازدید")]
        [DataType(DataType.DateTime)]
        public DateTime VisitDate { get; set; }

        public virtual Users? Users { get; set; } = null;
        public virtual Posts? Posts { get; set; } = null;
    }
}
